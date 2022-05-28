# Shakecraft: NLP text generator with TensorFlow and Flask 

This app contains an NLP model, Shakecraft, trained on the writings of
William Shakespeare and H. P. Lovecraft. Inputs are a 
starting seed string and number of characters to predict.
Shakecraft only predicts a single character at a time.

# [The app can be found here](https://shakecraft.herokuapp.com/)

*Note: Heroku does not have GPU support for TensorFlow and the 
app's slug size is surprisingly large. Therefore the site may take
a while to load and to generate text.*

H. P. Lovecraft's works can be found [here](https://www.hplovecraft.com/writings/texts/)

William Shakespeare's works can be found [here](https://www.thecompleteworksofshakespeare.com/)

## What's in this repo?

Here you can find an ipython notebook containing the code to
create and train the model.

Under the `app` directory you can find the things required
to deploy the app on Heroku. Note that the model itself is
not in this directory, as it is quite spacious.

