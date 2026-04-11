class User(BaseModel):
    """
    User entity with SQLAlchemy mapping and password hashing.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship(
        'Place',
        backref='owner',
        lazy=True,
        cascade='all, delete-orphan'
    )

    reviews = db.relationship(
        'Review',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # ================= INIT =================
    def __init__(self, **kwargs):
        """Initialize a new User."""
        password = kwargs.pop('password', None)

        super().__init__(**kwargs)

        if self.email and not _EMAIL_RE.match(self.email):
            raise ValueError("email must be a valid email address")

        if password:
            self.hash_password(password)

    # ================= PASSWORD =================
    def hash_password(self, password: str) -> None:
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Checks password validity."""
        return bcrypt.check_password_hash(self.password, password)

    # ================= BUSINESS =================
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # ================= SERIALIZATION =================
    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        })
        return base_dict

    def __str__(self):
        return f"[User] {self.email}"

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"
