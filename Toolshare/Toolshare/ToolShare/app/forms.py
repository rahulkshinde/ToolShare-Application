#"""
#Name: forms.py
#Description: This file is responsible for configuring the form elements that are to be rendered along with the HTML templates
#"""


from django import forms
from datetime import date,datetime
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from app.models import Profile, Sharezone
from app.StaticData import StaticData
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.forms.extras.widgets import SelectDateWidget
from app.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
import re
#Class Name: BootstrapAuthenticationForm
#Description: Authentication form which uses boostrap CSS
#"""

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

#========= Pooja ===========
#=========== Profile form =======
#"""
#Class Name: Profileform
#Description: This class handles all the form elements related to Profile page
#"""
class Profileform(forms.Form):
    numeric= RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')
    alphabets = RegexValidator(r'^[a-zA-Z_]*$', 'Only alphabet characters are allowed.')
    alphanumeric = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.')
    ##First Name made a non - editable field to ensure user that the user is not able to change the first name and in line with the requirements
    FirstName=forms.CharField(max_length=30,required=True, widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}))
    ##Middle Name made a non - editable field to ensure user that the user is not able to change the first name and in line with the requirements
    MiddleName=forms.CharField(max_length=30,required=False,widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}))
    ##Last Name made a non - editable field to ensure user that the user is not able to change the first name and in line with the requirements
    LastName=forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class':'disabled', 'readonly':'readonly'}))
    Gender1 = forms.ChoiceField(choices=StaticData.gender,required=True)
    PhoneNumber=forms.IntegerField(required=True, widget=forms.TextInput({'class': 'form-control'}),validators=[numeric])
    Address11=forms.CharField(max_length=30,required=True,widget=forms.TextInput({'class': 'form-control'}))
    Address12=forms.CharField(max_length=30,required=False,widget=forms.TextInput({'class': 'form-control'}))
    Email = forms.EmailField(max_length=30,widget=forms.EmailInput({'class': 'form-control',}),required=True)
    #DateofBirth1 = forms.DateField(widget = SelectDateWidget(years = range(datetime.now().year, datetime.now().year-100, -1)))
    Country11 = forms.ChoiceField(choices=StaticData.country,required=True)
    City11=forms.CharField(max_length=30,required=True, widget=forms.TextInput({ 'class': 'form-control'}),validators=[alphabets])
    State11 = forms.ChoiceField(choices=StaticData.us_states,required=True)
    ZipCode=forms.IntegerField(required=True,widget=forms.TextInput({'class': 'form-control'}),validators=[numeric])
    def clean_first_name(self):
        FirstName = self.cleaned_data['FirstName'].strip()
        if FirstName == '':
            raise forms.ValidationError("Spaces not allowed")
        return FirstName
    def clean_middle_name(self):
        middle_name_before_strip = self.cleaned_data['middle_name']
        MiddleName = self.cleaned_data['MiddleName'].strip()
        if (middle_name_before_strip != MiddleName):
            if MiddleName == '':
                raise forms.ValidationError("Spaces not allowed")
            return MiddleName
        else:
            return MiddleName
        def clean_last_name(self):
            LastName = self.cleaned_data['LastName'].strip()
            if LastName == '':
                raise forms.ValidationError("Spaces not allowed")
        return LastName
        def clean_address1(self):
            Address11 = self.cleaned_data['Address11'].strip()
            if Address11 == '':
                raise forms.ValidationError("Spaces not allowed")
        return Address11
        def clean_address2(self):
            address2_before_strip = self.cleaned_data['Address12']
            Address12 = self.cleaned_data['Address12'].strip()
            if (address2_before_strip != Address12):
                if Address12 == '':
                    raise forms.ValidationError("Spaces not allowed")
                return Address12
            else:
                return Address12
        def clean_city(self):
            City11 = self.cleaned_data['City11'].strip()
            if City11 == '':
                raise forms.ValidationError("Spaces not allowed")
            return City11
        def clean_Email(self):
            Email = self.cleaned_data['Email'].strip()
            if Email == '':
                raise forms.ValidationError("Spaces not allowed")
            return Email

#============= Pooja ==========
#======= Preference of User =======
#"""
#Class Name: PreferencesForm
#Description: This class handles all the form elements related to user preferences
#"""

class PreferenceForm(forms.Form):
    PickUpArrangements = forms.ChoiceField(choices=StaticData.PickUpArrangement,required=True)
    RemainderFrequency1= forms.ChoiceField(choices=StaticData.RemainderFrequency,required=True)
    RemainderType1 = forms.ChoiceField(choices=StaticData.RemainderTypes,required=True)

#"""
#Class Name: ShedForm
#Description: This class handles all the form elements related to shed page
#"""

class ShedForm(forms.Form):

    Name1=forms.CharField(max_length=254,required=True,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Shed Name'}))
    Address1=forms.CharField(max_length=254,required=True,
                               widget=forms.TextInput({
                               'class': 'form-control',
                                'placeholder': 'Enter Address1'}))
    Address2=forms.CharField(max_length=254,required=False,
                               widget=forms.TextInput({
                               'class': 'form-control',
                               'placeholder': 'Enter Address2'}))
#"""
#Method Name: is_valid
#Description: This method handles shed validation
#"""

    def is_valid(self,dup):
        valid = super(ShedForm, self).is_valid()
        if not valid:
            return valid
        flag=True
        if dup=='yes':
            self._errors['Name1'] = 'shed with this name is already exist'
            flag=False
        if self.cleaned_data['Name1'].strip()=='':
            self._errors['Name1'] = 'shed Name cannot be blank'
            flag=False
        if  self.cleaned_data['Address1'].strip()=='':
            self._errors['Address1'] = 'shed Address cannot be blank'
            flag=False
        return flag

#"""
#Class Name: signUp
#Description: This class handles all the form elements related to user registration page
#"""

# Create form class for the Registration form
class signUp(forms.Form):
  alphabets = RegexValidator(r'^[a-zA-Z_]*$', 'Only alphabet characters are allowed.')
  alphanumeric = RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.')
  alphabets_spaces = RegexValidator(r'^[a-zA-Z ]*$', 'Only alphabet characters and spaces are allowed.')
  first_name = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'First Name'}),required=True,validators=[alphabets_spaces])
  middle_name = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Middle Name'}),required=False,validators=[alphabets_spaces])
  last_name = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Last Name'}),required=True,validators=[alphabets_spaces])
  city      = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'placeholder': 'Your City'}),required=True,validators=[alphabets_spaces])
              
  address1  = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'placeholder': 'Address 1'}),required=True)
                                                                                    
  address2  = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'placeholder': 'Address 2'}),required=False)
  
  username = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Username'}),required=True)
  
  email = forms.EmailField(max_length=30,widget=forms.EmailInput({
                                   'class': 'form-control','placeholder': 'Your Email'}),required=True)

  PhoneNumber = forms.IntegerField(widget=forms.TextInput({
                                   'class': 'form-control','placeholder': 'Your Phone'}),required=True, error_messages={'invalid':'Invalid phone number'})
  pickuparrangement = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Pickup Arrangement'}),required=True,validators=[alphabets_spaces])

  zipcode = forms.IntegerField(widget=forms.TextInput({
                                   'class': 'form-control','placeholder': 'Your Zipcode'}),required=True)
  
  dateofbirth = forms.DateField(('%d/%m/%Y',),  required=True,  
        widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
            'class':'input','placeholder': 'Your Date of Birth dd/mm/yyyy'})
    )
     
  
  dateofbirth =forms.DateField(widget = SelectDateWidget(years = range(datetime.now().year, datetime.now().year-100, -1)))

  state = forms.ChoiceField(choices=StaticData.us_states,required=True)
  country = forms.ChoiceField(choices=StaticData.country,required=True)
  gender = forms.ChoiceField(choices=StaticData.gender,required=True)
  password1  = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput({
                                   'placeholder': 'Enter Password'}),required=True,validators=[alphanumeric])
  password2  = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput({
                                   'placeholder': 'Re-enter Password'}),required=True,validators=[alphanumeric])

#"""
#Method Name: Clean_DataofBirth
#Description: This method checks if A persons age is older than 15 years
#"""  
  def clean_dateofbirth(self):
      dateofbirth = self.cleaned_data['dateofbirth']
      print (datetime.now() + timedelta(days=-5475))
      d = (datetime.now() + timedelta(days=-5475))
      print (d.strftime("%Y-%m-%d"))
      e=d.strftime("%Y-%m-%d")
      if (date.strftime(dateofbirth,"%Y-%m-%d") >= e):
          raise forms.ValidationError('Must be older than 15 years i.e. Date of birth must be older than %(value)s',params={'value':e},)
      return dateofbirth

  
    #"""
    #Method Name: clean_username
    #Description: This method handles the check whether user exists already
    #"""
  def clean_username(self):
       username = self.cleaned_data['username'].strip()
       if User.objects.filter(username=username).exists():
        raise forms.ValidationError("Username already exists")
       if username == '':
          raise forms.ValidationError("Spaces not allowed")
       return username
    #"""
    #Method Name: clean_password2
    #Description: This method handles the check whether both the passwords are the same
    #"""
  def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2
    #"""
    #Method Name: clean_first_name
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()
        if first_name == '':
            raise forms.ValidationError("Spaces not allowed")
        return first_name
    #"""
    #Method Name: clean_middle_name
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_middle_name(self):
        middle_name_before_strip = self.cleaned_data['middle_name']
        middle_name = self.cleaned_data['middle_name'].strip()
        if (middle_name_before_strip != middle_name):
            if middle_name == '':
                raise forms.ValidationError("Spaces not allowed")
            return middle_name
        else:
            return middle_name
    #"""
    #Method Name: clean_last_name
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].strip()
        if last_name == '':
            raise forms.ValidationError("Spaces not allowed")
        return last_name
    #"""
    #Method Name: clean_address1
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_address1(self):
        address1 = self.cleaned_data['address1'].strip()
        if address1 == '':
            raise forms.ValidationError("Spaces not allowed")
        return address1
    #"""
    #Method Name: clean_address2
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_address2(self):
        address2_before_strip = self.cleaned_data['address2']
        address2 = self.cleaned_data['address2'].strip()
        if (address2_before_strip != address2):
            if address2 == '':
                raise forms.ValidationError("Spaces not allowed")
            return address2
        else:
            return address2
    #"""
    #Method Name: clean_city
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_city(self):
        city = self.cleaned_data['city'].strip()
        if city == '':
            raise forms.ValidationError("Spaces not allowed")
        return city
    #"""
    #Method Name: clean_pickuparrangement
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
  def clean_pickuparrangement(self):
        pickuparrangement = self.cleaned_data['pickuparrangement'].strip()
        if pickuparrangement == '':
            raise forms.ValidationError("Spaces not allowed")
        return pickuparrangement

#"""
#Class Name: RegisterToolForm
#Description: This class handles all the form elements related to tool registration page
#"""
class RegisterToolForm(forms.Form):
   alphabets = RegexValidator(r'^[a-zA-Z_ ]*$', 'Only alphabet characters are allowed.')
   alphanumeric = RegexValidator(r'^[a-zA-Z0-9 ]*$', 'Only alphanumeric characters are allowed.')
   Toolname = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Tool Name'}),required=True,validators=[alphabets])
  
   Description = forms.CharField(widget=forms.Textarea(attrs={'cols': 80, 'rows': 6,'width':400}),required=True,validators=[alphabets])

   Category = forms.ChoiceField(choices=StaticData.Category,required=True)
  
   UniqueAttribute = forms.CharField(max_length=30,widget=forms.TextInput({'class': 'form-control','placeholder': 'Enter a unique attribute for your tool','id':'unique'}),required=True,validators=[alphabets])
  
   pickuparrangement =forms.ChoiceField(widget=forms.Select,choices=StaticData.PickUpArrangement,required=True)

   #status = forms.CharField(max_length=30,widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Enter Tool Name'}),required=False,initial='Available')
  
   availability = forms.CharField(max_length=10,widget=forms.TextInput)

   address1  = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Tool Address1'}),required=False)
                                                                                    
   address2  = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Address2'}),required=False)
   stuff_image =forms.ImageField(label=_('Choose Image'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)

    #"""
    #Method Name: clean_Toolname
    #Description: This method checks whether the field is filled completely with spaces
    #"""       
   def clean_Toolname(self):
        Toolname = self.cleaned_data['Toolname'].strip()
        if Toolname == '':
            raise forms.ValidationError("Spaces not allowed")
        return Toolname
    #"""
    #Method Name: clean_Description
    #Description: This method checks whether the field is filled completely with spaces
    #"""     
   def clean_Description(self):
        Description= self.cleaned_data['Description'].strip()
        if Description == '':
            raise forms.ValidationError("Spaces not allowed")
        return Description
   
   def clean_UniqueAttribute(self):
        UniqueAttribute = self.cleaned_data['UniqueAttribute'].strip()
        if UniqueAttribute == '':
            raise forms.ValidationError("Spaces not allowed")
        return UniqueAttribute
   
   
    #"""
    #Class Name: resetPasswordForm
    #Description: This class handles the functionality of password
    #"""     
# Rahul Shinde   
class resetPasswordForm(forms.Form):
       userName = forms.CharField(max_length=30,widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Your Registered User Name'}),required=True)
       def is_valid(self):
           if super(resetPasswordForm, self).is_valid():
               uname=self.cleaned_data['userName']
               try:
                   User.objects.get(username=uname)
                   return True
               except User.DoesNotExist:
                   self._errors['userName'] = 'The username does not exist'
                   return False
    #"""
    #Class Name: updatePasswordForm
    #Description: This class handles the functionality of password update
    #"""     
# Rahul Shinde
class updatePasswordForm(forms.Form):

   oldPassword = forms.CharField(max_length=30,widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter Your Old Password'}),required=True)
   newPassword = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Enter New Password (Min. 6 Chars)'}),required=True)
   newPassword1 = forms.CharField(min_length=6,max_length=30,widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Confirm Password (Min. 6 Chars)'}),required=True)
    #"""
    #Method Name: is_valid
    #Description: This method checks whether the password and confirm password are same
    #"""     
   def is_valid(self):
       if super(updatePasswordForm, self).is_valid():
           oldPwd=self.cleaned_data['oldPassword']
           newPwd=self.cleaned_data['newPassword']
           newPwd1=self.cleaned_data['newPassword1']
           if newPwd == newPwd1:
               return True
           else:
               self._errors['newPassword'] = 'Passwords does not match'
               return False
       return False
#======= Change Tool Availability=======
#"""
#Class Name: updateToolForm
#Description: This class handles all the form elements related to tool update
#"""
choices1 = ( (1,'Yes'),
            (0,'No'),
          )

class updateToolForm(forms.Form):
    availability1 = forms.TypedChoiceField(
                         choices=choices1, widget=forms.RadioSelect, coerce=int
                    )



 