from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import Bill, Customer, BillItem
from app.main.forms import BillForm, BillItemForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    # Dashboard statistics
    total_bills = Bill.query.count()
    pending_bills = Bill.query.filter(Bill.status != 'paid').count()
    recent_bills = Bill.query.order_by(Bill.date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_bills=total_bills,
                         pending_bills=pending_bills,
                         recent_bills=recent_bills)

@bp.route('/bills')
@login_required
def list_bills():
    page = request.args.get('page', 1, type=int)
    bills = Bill.query.order_by(Bill.date.desc()).paginate(page=page, per_page=10)
    return render_template('bills/list.html', bills=bills)

@bp.route('/bill/create', methods=['GET', 'POST'])
@login_required
def create_bill():
    form = BillForm()
    if form.validate_on_submit():
        customer = Customer(name=form.customer_name.data, 
                          phone=form.customer_phone.data)
        db.session.add(customer)
        db.session.commit()
        
        bill = Bill(bill_number=form.bill_number.data,
                   customer_id=customer.id,
                   user_id=current_user.id,
                   total_amount=0)  # Will be updated with items
        db.session.add(bill)
        db.session.commit()
        
        flash('Bill created! Now add items.', 'success')
        return redirect(url_for('main.add_bill_items', bill_id=bill.id))
    
    return render_template('bills/create.html', form=form)

@bp.route('/bill/<int:bill_id>/items', methods=['GET', 'POST'])
@login_required
def add_bill_items(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    form = BillItemForm()
    
    if form.validate_on_submit():
        amount = form.quantity.data * form.rate.data
        item = BillItem(description=form.description.data,
                       quantity=form.quantity.data,
                       rate=form.rate.data,
                       amount=amount,
                       bill_id=bill.id)
        db.session.add(item)
        
        # Update bill total
        bill.total_amount += amount
        db.session.commit()
        
        flash('Item added!', 'success')
        return redirect(url_for('main.add_bill_items', bill_id=bill.id))
    
    return render_template('bills/add_items.html', bill=bill, form=form)
