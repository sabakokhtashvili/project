from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'lukamegreladze-mepitone'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text)

    def __repr__(self):
        return f'<Book {self.title}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    return render_template('4index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('აუცილებელია ველების შევსება!', 'error')
        else:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('დაკავებულია, გთხოვთ სხვა სახელი სცადოთ', 'error')
            else:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                flash('რეგისტრაცია წარმატებულია!', 'success')
                return redirect(url_for('book_list'))

    return render_template('4register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('წარმატებით შეხვედით!', 'success')
            return redirect(url_for('book_list'))
        else:
            flash('არასწორი username ან password. გთხოვთ სცადოთ თავიდან.', 'error')

    return render_template('4login.html')


@app.route('/books')
def book_list():
    books = Book.query.all()
    return render_template('4book_list.html', books=books)


@app.route('/books/<int:book_id>')
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('4book_details.html', book=book)


@app.route('/books/search', methods=['GET', 'POST'])
def book_search():
    if request.method == 'POST':
        search_query = request.form.get('search')
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).all()
        return render_template('4book_search.html', books=books, search_query=search_query)

    return render_template('4book_search.html', books=None, search_query=None)


@app.route('/books/add', methods=['GET', 'POST'])
def book_add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        review = request.form.get('review')

        if not title or not author:
            flash('აუცილებელია ველების შევსება!', 'error')
        else:
            new_book = Book(title=title, author=author, review=review)
            db.session.add(new_book)
            db.session.commit()
            flash('წიგნი წარმატებით დაემატა!', 'success')
            return redirect(url_for('book_list'))

    return render_template('4book_add.html')




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
