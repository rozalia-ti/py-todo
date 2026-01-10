from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import func, or_
from extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    from models import User, Note
    # Получаем статистику для главной страницы
    stats = db.session.query(User.username, func.count(Note.id)).outerjoin(Note).group_by(User.id).all()
    return render_template('index.html', stats=stats)

@main.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    from models import User
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegistrationForm
    from models import User
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/dashboard')
@login_required
def dashboard():
    from models import Note
    # Реализация поиска по ТЗ
    q = request.args.get('q', '')
    if q:
        notes = current_user.notes.filter(or_(
            Note.title.contains(q), 
            Note.body.contains(q), 
            Note.tags.contains(q)
        )).all()
    else:
        notes = current_user.notes.all()
    return render_template('dashboard.html', notes=notes)



@main.route('/note/new', methods=['GET', 'POST'])
@login_required
def create_note():
    from forms import NoteForm
    from models import Note
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            body=form.body.data,
            tags=form.tags.data,
            author=current_user
        )
        db.session.add(note)
        db.session.commit()
        flash('Заметка создана!')
        return redirect(url_for('main.dashboard'))
    return render_template('create_note.html', form=form, title='Новая заметка')

@main.route('/note/<int:note_id>/delete', methods=['POST'])
@login_required
def delete_note(note_id):
    from models import Note
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        flash('У вас нет прав для удаления этой заметки.')
        return redirect(url_for('main.dashboard'))
    db.session.delete(note)
    db.session.commit()
    flash('Заметка удалена.')
    return redirect(url_for('main.dashboard'))

@main.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    from models import Note
    from forms import NoteForm
    # Находим заметку или выдаем 404, если её нет
    note = Note.query.get_or_404(note_id)
    
    # Проверка прав доступа
    if note.author != current_user:
        flash('Вы не можете редактировать чужие заметки!')
        return redirect(url_for('main.dashboard'))
    
    form = NoteForm()
    
    # Если форма отправлена (POST), обновляем данные
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        note.tags = form.tags.data
        db.session.commit()
        flash('Заметка обновлена!')
        return redirect(url_for('main.dashboard'))
    
    # Если это просто переход по ссылке (GET), заполняем форму текущими данными
    elif request.method == 'GET':
        form.title.data = note.title
        form.body.data = note.body
        form.tags.data = note.tags
        
    return render_template('create_note.html', form=form, title='Редактирование заметки')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('main.index'))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_password = request.form.get('password')
        if new_password:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Пароль успешно изменен!', 'success')
            return redirect(url_for('main.profile'))
    return render_template('profile.html')