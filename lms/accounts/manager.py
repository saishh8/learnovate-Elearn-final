from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email , password , **extra_fields):

        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_instructor",False)
        extra_fields.setdefault("is_learner",False)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("super user must have is_staff true"))
        
        return self.create_user(email, password , **extra_fields)

    def create_learner(self, email , password , **extra_fields):

        extra_fields.setdefault("is_superuser",False)
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_instructor",False)
        extra_fields.setdefault("is_learner",True)

        if extra_fields.get("is_learner") is not True:
            raise ValueError(("Learner must have is_learner true"))
        
        return self.create_user(email, password , **extra_fields)

    def create_instructor(self, email , password , **extra_fields):

        extra_fields.setdefault("is_superuser",False)
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_instructor",True)
        extra_fields.setdefault("is_learner",False)

        if extra_fields.get("is_instructor") is not True:
            raise ValueError(("Instructor must have is_instrucor true"))
        
        return self.create_user(email, password , **extra_fields)