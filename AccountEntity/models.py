
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone


class AccountEntityManager(BaseUserManager):
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return None
        try:
            user = self.get(username=username)
            print(user.check_password(password))
        except self.model.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None
    def create_user(self, username, account_name,sdt="", email=None, password=None):
        if email:
            email = self.normalize_email(email)
            
        user = self.model(username=username, email=email, account_name=account_name,sdt=sdt)
        user.set_password(password)  # Mã hóa mật khẩu trước khi lưu
        user.save(using=self._db)
        return user

    def create_superuser(self, username,account_name, email, password):
        user = self.create_user(username=username, email=email, account_name=account_name, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class AccountEntity(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255,null=True, unique=True)
    create_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=True)
    account_name = models.CharField(max_length=255)
    img_user = models.TextField(default="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAA9lBMVEX///8VGEXtJCoAADyAgpEGCj9gYnVSVGv8//8AAC/tAAAAADX+/v8AADoAADAIDUEAACgAADO9vsf08/TW1t5sbYEAACwAABvOztTtAA7sJConKVFQVHG3uMDq6e0AACSHiJjc3eDsExxpa3/sAAr76ul0dYitrrr99/b84N/519XzgIP2x8YaHUrtWVvtFBz3zc4AAB82N1kAAED3vb30bm/zeXn96O30i4z4o6XzqajtNzzxUVXuRUfzhIb0t7X0YWXtMDXzk5RBRF5MT2b0c3j5sLP4pqmam6kAABE6PV86OlwrLE8RFkBbX3qfoKoAAACLiKDk6WADAAAKPElEQVR4nO2dDVeqShfHp8lqRDQFUzAjxTfsjfKUtzIz7VYeT9fu/f5f5pnhTVNQbEUwPPNf6ywRgbN/7WHvmc0AADAxMTExMTExMTExMTExUSCEwrYgaGnXYVsQsNBNI2wTAhUC3b/CtiFQIXB7GbYNAevuPmwLAtb1LeDDtiFQnTzEPFM0oBZvQq13ErYJAesh5qkedU/DNiFg3fXCtiBYoWtVC9uGQIXacsyjjAbvYp7qL27inQjBKOZRBgy4eA8JQZuL+YBCU1/CNiFQIXDRj3cUBaOYn4TomruOd6JocI9hmxCw+r14d0fBKRfz0tqAuw3bhECFBxT9sG0IVqgnt8O2IUjxqMu9hW1EsBpwT/HOhG017nWLB24QbxfecjexrlugM24Y7zbaGMpnYdsQpHh0w8W8wH3PDeMdZdp1+STOhAj0uVHYRgSrEfcQ71lBl7Ie78qM1pPvwrYhWHV1GO9cf8bVY53rgVbSb+McZRBuozEvXJzVuXhPuNCg/hS2DcGqq5diHUfRWV2O9ZVCpPXUeIcZ9KjHuz6K+6NqZIe9yvOel/6u+D5KD8qR7XEr2Z3P2neUrvk8BhrJEQ4zSm7L1rkh5+vWjl/Cth7lMMMrnyXu7W9IiMCTSlV1bXdnUx8OZPUFUNTlnhGmD3ztoMEIhxk3bUzY1SMcZty0KeEJBymbm7cpYR/WB0Hb9L3akPBNVi8oijJEmxE2INRpm1SyGWFXVZ+Ctui7tREhDjNcm7JGuhlhH+qRHVN4ahPCVxmqVCV7QxsQakMoj2hroxsR3uqQxumH/gnbOpRff8aob9UcYXPVdjy40SGVF7T9EpJMUadyYpBfQtSHMMIj+xXyS4gzBVUj+5lmhNurCLUehJTene2T8A67kNJ7DfwRapDWs9DveYiTvU5X7WImX4QNGY8Lf9Cob5Uvwq4KZWoncvshxP01SO+8krlIk/Da5kWFOr3T13wQnsiwROG40NZ6QnSjwuheLlyv9YRtDgdSih8isJ7wSaW2w2ZoDSFPzkJI9fy1dT4kZyEc/rRV36l1hCQXUpwqwHpC3J2h7HrhotYQkh6p+kL1XO7VhOgUN1JKx/a2VhNqddwjpbFIOqfVhCPq48waQq2EXUj7DLZVhOiNxJmHMMz6Rq0i5PvYhTqNlfx5rSK8JnFGpzvOrCa8wNle7YZh1XdqBWGbK1GfDMFKwlPsQkj/Pb7ehBqpP9E8uLfkTUhSBZRpmz2zLE9CcjktDo3UkxBdEhfqpzSPKkx5+pAMDGGd/kbqSdgggFAOy6xvlBfhPWmk6kVYZn2jvAiNOEPv5Zg5eRCSMjCEHMWFYEcehLck3cNY3IDnQTgkgGosHifrTnhpuDAed9u7E56auSIOp6E7IZk9Q7psVFeCbbkSGj22r2ZDxEfroVGuhI9GI9W/9CREFLXioyuh2UjlL91v343aE3ncCM10/6ULv+glcn11N8I7I1fAr7xmBANG6yx0J+ybgF+YyHYTwbqVC6FmNtLN64gokq8mcSE8q5uEG/ZokNaP5CxpF8JT8zSUN7wLrzGM5m17y4TIOg03q2CgtvoaRQ+6EbZNQLjJA9Z5cMJF9QrOMuGZbBJuNKH0motmEwVuhLf6pskCobsIP3B+mfBJNUOp30cD8wh0o/y08iVCbWi60P+rKrSHKAMuE7brJZPQ53sAULsEIz1SXiJ8tQONz1HQQC9F+8bZJUI70PghxGSPXC/ilYBFQmQFGn8+bPS5Cy3ic8KWfGgFGky41nB0rXLdaOOBZcIGZxGuv/rLn8o0vPJhkfBatglX16EQuuzJVLzdaZHw3go0WCvaHwLaKaeqERzvLsubcGXP+2yoq8NIp0FHi4R3DqHuPWBvvOhQvoh4lrC1SDhyCNUnj134karDOjWvPvIm9Kom3kOdqvl8i4RvM0K3Z+1og74MS3r/JHJFQ08tEg5kOHPi42dE1B4Nyc9cl6YXNi8SXnIzQijfOBeBcX4YPNSxg0uqGsWaobcWCfk5H+KGWhqdtRuNRvvy7UU3f6k/URJDbS31vPvzhCWoy3VZxv90a+RP38M/Fgh5cKtCb3G0ORC4jfFlTz69R9cZaGq5EvWoe/DBEZWTT5YJrYv4i3zcY4OiFDGnJUKevILrM10Jqnr3r5AN/bLcrh82Lj6nDLk3akS8VLFCrtfx0euwbmUHvQ67Z1Sef7b2kilLhRkhD/jr0x7HccObu8uoV5rWSRJsHUlh28LE9P8q0RaPRBGZa5D1Cz//6axWFBHN7c7PLSuiuH6Xn1btqpDZ2U4WrsbieUbAK5R0Mk9+aKWtx9CX0+8K/nhOHpG15UKxeHVYMUmAsvWrah1IrBxeFX+n9sgx3tMTssF7AQcv/mNS+F087ozDKgoo1aqQ2ZaqVVE8tAgLhFA8T28Z30F5J32I7S0TwlrmXVAU6U+xY+5d3U7lreO8Z6Z5UWntZ8cAdPbTHQzUIYTT5ERQROH9dzkcQMPMZJo4STxMtRRFyZs+bCYTQvKceKK808m9iwahUEiRLQGvWLsqDmEzMzE+pdR2FXRyfzITHnSSEmgVjIPglvrDVPNyCLdymWQy808GG53PYsOmOfJgpXLuqJKd8IRwnHrGrhknEpWEafCMsJyqmGu2MFYnJzSPy+APXmzmpnhthewihgFnyCHMzXz4nO4kEmWjwZYzLdDMTp9zR6BleHXcbOayJhgmtM7DWnpqfOa38e6dpAB2j2vEhx+Zd54QNlPH4XnRIZxFmlbuMNFsJvZSE3ICtgA4KGyljgB/mNklnhAyM0LLbqmQGpNjTTJ7wCDkp8l/MhIQt3JNsksrVMJi1iDcvzIIj4t5JXdsBBlxq1gBz0VMCGrZYxxpxIN0cXu/mD1vmk2umk1ms8fHx/9ixD+F4n6u+CuBXXZYJLtPk0UcaZRauvhru5g9TIRXYRUlifznvCSJ1ociWX3UKl7IS4q52vCBIh21hDw/29WUsbHQOjI3yjtHWt6FiYmJKYYScBisWHFOTODvdk96bHVB8jhXVFvWymZtOrXWi81p7cM+ilibHNnLLSvvKdNazd74P7xu9aOmg1MLW7ZnLYu/cR/ErmUcWIaKuMf8IVgry/m8HfbFaVWp2RsnBPHZTugV62/E5yvjqrWxdACESlAIa0QIp9ayWJ7OCJu2xdgPzrBgOttRxD5p2b6t5YGySIh/Fpyty8o0rG7pJ8JmRVombAmi08Am0z37rVDic6Uysa2u/vrbqWO5EubfnRb90zII7YZ3IJaXCcWmZLsKlKtVZ8Q7lXbnqnP5if3FlRCUQxtZCC3cR7aWxQMwfrZGQzNC0PzPWZxvpQdAnNi1CdyMJdtJ7oS10AiVQyExtpbFGuCzNuGBgzXec7aefHx82BFoF8PYVOMDYWKDJWaETnw1zuawVB07diDc0CQbTHJMUmaN8ajValnrebxWdJx0NLb/MnM7VufGSxLreTMxMTExMTExMTExMTExMTExMTExMa3Q/wCyYfnjNgmX4AAAAABJRU5ErkJggg==")
    sdt = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    objects = AccountEntityManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    @property
    def is_staff(self):
        return self.is_superuser