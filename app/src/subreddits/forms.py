from django import forms
from subreddits.query import validate_subreddit
SEARCH_BY = (
    ('new', 'New'),
    ('hot', 'Hot'),
    ('top', 'Top')
)

class SubredditForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter the name of a valid subreddit"}))
    search_by = forms.ChoiceField(choices=SEARCH_BY)
    number_of_submissions = forms.IntegerField(label="Number of Posts", help_text="Limit=30", min_value=1, max_value=30)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate = validate_subreddit(name)
        if validate != name:
            raise forms.ValidationError(f"{name} is not a valid subreddit")
        else:
            return name