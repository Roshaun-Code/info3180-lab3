from app import app
from flask import render_template, request, redirect, url_for, flash
from app.forms import ContactForm
from app import mail
from flask_mail import Message



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message("New Contact Form Submission",
                      sender=("Sender Name", "your_email@example.com"),
                      recipients=["recipient@example.com"])
        msg.body = f"Message from {form.name.data}:\n\n{form.message.data}"
        
        try:
            mail.send(msg)
            flash(f'Message from {form.name.data} sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f'Error sending message: {str(e)}', 'danger')
            return redirect(url_for('contact'))
    
    flash_errors(form)  # Flash errors if validation fails
    return render_template('contact.html', form=form)


###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
