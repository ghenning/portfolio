from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms import validators
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, GRU, Dense
from tensorflow.keras.losses import sparse_categorical_crossentropy
import tensorflow as tf
from things_for_app import vocab_size,embed_dim,rnn_neurons,batch_size
from things_for_app import char_to_idx,idx_to_char


app = Flask(__name__)
app.config['SECRET_KEY'] = 'meow'

def sparse_cat_loss(y_true,y_pred):
    return sparse_categorical_crossentropy(y_true,y_pred,from_logits=True)

def create_model(vocab_size,embed_dim,rnn_neurons,batch_size):
    model = Sequential()
    model.add(Embedding(vocab_size,embed_dim,batch_input_shape=[batch_size,None]))
    model.add(GRU(rnn_neurons,return_sequences=True,stateful=True,
                 recurrent_initializer='glorot_uniform'))
    model.add(GRU(rnn_neurons,return_sequences=True,stateful=True,
                 recurrent_initializer='glorot_uniform'))
    model.add(Dense(vocab_size))
    model.compile(optimizer='adam',loss=sparse_cat_loss)
    return model

def load_model(vocab_size,embed_dim,rnn_neurons):
    tmp_model = create_model(vocab_size,embed_dim,rnn_neurons,batch_size=1)
    tmp_model.load_weights('shakecraft_gen3.h5')
    #tmp_model.load_weights('shakecraft_gen2.h5')
    tmp_model.build(tf.TensorShape([1,None]))
    return tmp_model

def generate_text(model, start_seed,gen_size,temp=1.0):

    num_generate = gen_size
    input_eval = [char_to_idx[s] for s in start_seed]
    input_eval = tf.expand_dims(input_eval, 0)
    text_generated = []
    temperature = temp
    model.reset_states()

    for i in range(num_generate):

        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0)
        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()
        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx_to_char[predicted_id])

    return (start_seed + ''.join(text_generated))

class inputs(FlaskForm):
    start_seed = StringField("Start the story here:",
                    default = "The old man kept yelling at the clouds.")
    story_len = SelectField(label="Story length (in characters)",
            choices=[300,700,1200,1800,2500,4000])

    submit = SubmitField("Write me a story!")


@app.route('/',methods=['GET','POST'])
def index():
    form = inputs()
    if form.validate_on_submit():
        session['start_seed'] = form.start_seed.data
        session['story_len'] = int(form.story_len.data)

        return redirect(url_for("testing"))

    return render_template('index.html',form=form)

@app.route('/testing')
def testing():

    content = {}
    content['start_seed'] = session['start_seed']
    content['story_len'] = session['story_len']
    model = create_model(vocab_size,embed_dim,rnn_neurons,batch_size)    
    model2 = load_model(vocab_size,embed_dim,rnn_neurons)
    results = generate_text(model2,content['start_seed'],
                            gen_size=content['story_len'])

    return render_template('testing.html',results=results)

if __name__ == "__main__":
	app.run()
