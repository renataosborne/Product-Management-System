rom app import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from app.blueprints.blog.models import BlogPost
from sqlalchemy.dialects.postgresql import UUID
from flask_admin import Admin
from flask_login import UserMixin, LoginManager
from flask_admin.contrib.sqla import ModelView

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)



class Role(db.Model, RoleMixin):

    
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name

    
    def __hash__(self):
        return hash(self.name)




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def before_first_request():

    
    db.create_all()

   
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

  
    encrypted_password = utils.encrypt_password('password')
    if not user_datastore.get_user('someone@example.com'):
        user_datastore.create_user(email='someone@example.com', password=encrypted_password)
    if not user_datastore.get_user('admin@example.com'):
        user_datastore.create_user(email='admin@example.com', password=encrypted_password)

   
    db.session.commit()

    
    user_datastore.add_role_to_user('someone@example.com', 'end-user')
    user_datastore.add_role_to_user('admin@example.com', 'admin')
    db.session.commit()


    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_hashed_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'username', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            
            
        }
        return data

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class UserAdmin(sqla.ModelView):

    
    column_exclude_list = list = ('password',)

   
    form_excluded_columns = ('password',)

   
    column_auto_select_related = True

    
    def is_accessible(self):
        return current_user.has_role('admin')

    def scaffold_form(self):

        
        form_class = super(UserAdmin, self).scaffold_form()

        
        form_class.password2 = PasswordField('New Password')
        return form_class

    
    def on_model_change(self, form, model, is_created):

       
        if len(model.password2):

            
            model.password = utils.encrypt_password(model.password2)



class RoleAdmin(sqla.ModelView):

   
    def is_accessible(self):
        return current_user.has_role('admin')


admin = Admin(app)


admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))


