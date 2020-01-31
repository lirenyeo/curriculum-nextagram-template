from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user
from models.user import User
from models.post import Post
from models.endorsement import Endorsement
from app import gateway

endorsements_blueprint = Blueprint('endorsements',
                                __name__,
                                template_folder='templates')

# endorsesement#new
# /endorsements/new/2
@endorsements_blueprint.route('/new/<post_id>')
def new(post_id):
    post = Post.get_by_id(post_id)
    client_token = gateway.client_token.generate()
    return render_template('endorsements/new.html', post=post, client_token=client_token)


@endorsements_blueprint.route('/<post_id>', methods=['POST'])
def create(post_id):
    nonce = request.form.get('nonce')
    amount = request.form.get('amount')


    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        endorsement = Endorsement(amount=amount, post_id=post_id)
        endorsement.save()

        # you should go to a success page with receipt
        flash('Payment received')
        return redirect('/')
    else:
        flash('Payment did not go through, please try again', 'danger')
        return redirect('/')


