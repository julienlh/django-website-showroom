import os, uuid
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Edition(models.Model):
    help_text = "Main title shown on page"
    site_title = models.CharField(max_length=40, help_text=help_text)
    help_text = "2-letter-country-code for showing a corresponding flag (e.g. 'de', 'en'). Careful, not existing code will break site."
    country = models.CharField(max_length=2, help_text=help_text)
    help_text = "Numeric value for edition order. Tip: Use 100-200-300-... steps for easy reordering. "
    help_text += "Edition first in order will be used as edition default."
    order = models.IntegerField(help_text=help_text)
    help_text = "Something like 'English version', used for mouseover on flag"
    short_description = models.CharField(max_length=40, help_text=help_text)
    help_text = "Used for html title tag"
    html_title = models.CharField(max_length=100, help_text=help_text)
    help_text = "Subtitle (HTML tags possible)"
    site_subtitle = models.CharField(max_length=125, help_text=help_text)
    help_text = "Title for rss feed"
    rss_title = models.CharField(max_length=100, help_text=help_text)
    help_text = "Description for rss feed"
    rss_description = models.CharField(max_length=200, help_text=help_text)
    help_text = "Optional, link to Facebook page"
    facebook_url = models.CharField(max_length=90, blank=True, null=True, help_text=help_text)
    help_text = "Something like - e.g. - 'Home'"
    home_menu_title = models.CharField(max_length=40, help_text=help_text)
    help_text = "HTML color code, e.g. '#003300"
    home_menu_color = models.CharField(max_length=7, help_text=help_text)
    help_text = "HTML color code, e.g. '#006600"
    home_menu_active_color = models.CharField(max_length=7, help_text=help_text)
    help_text = "Number of websites for home category"
    home_num_websites = models.IntegerField(help_text=help_text)
    help_text = "Left footer (HTML tags possible)"
    footer_left = models.CharField(max_length=200, help_text=help_text)
    help_text = "Right footer (HTML tags possible)"
    footer_right = models.CharField(max_length=200, help_text=help_text)
    help_text = "Title of contact navi"
    contact_title = models.CharField(max_length=40, help_text=help_text)
    help_text = "Complete HTML content of contact page, with <p>, <br> and all that stuff"
    contact_html = models.TextField()
    comments = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.site_title + " (" + self.country + ")"


class Category(models.Model):
    name = models.CharField(max_length=40)
    url_name = models.SlugField(max_length=40, help_text="Every url-conform string except 'contact'")
    order = models.IntegerField(help_text="Numeric value for category order. Tip: Use 100-200-300-... steps for easy reordering.")
    color = models.CharField(max_length=7, help_text="Format: #ffffff")
    active_color = models.CharField(max_length=7, help_text="Format: #ffffff")

    ordering = ['order']

    def __unicode__(self):
        return self.name


def get_path(instance, filename):
    pos = filename.rfind('.')
    path = 'screenshots/' + 's_' + str(uuid.uuid1()) + filename[pos:]
    return path

class Website(models.Model):
    help_text = "Generic title, used if no extra edition specific title is provided"
    title = models.CharField(max_length=50, help_text=help_text)
    category = models.ForeignKey(Category)
    help_text = "DEPRECATED! Will be removed in the future, please ignore"
    order = models.IntegerField(help_text=help_text)
    help_text = "Optional, 2-letter-country-code for showing a corresponding flag (e.g. 'de', 'en'). Careful, not existing code will break site."
    country = models.CharField(max_length=2, null=True, blank=True, help_text=help_text)
    help_text = "DEPRECATED! Will be removed in the future, please ignore"
    desc = models.TextField(help_text=help_text)
    help_text = "Image file, size: 300x200, name will be unified. If you provide a larger file image will be resized (use same proportions, e.g. 600x400 or 750x500)."
    screenshot = models.ImageField(upload_to=get_path, help_text=help_text)
    url = models.CharField(max_length=90)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    ordering = ['category', 'order']

    def __unicode__(self):
        return self.title


@receiver(post_save, sender=Website)
def post_save_handler(sender, instance, using, **kwargs):
    from PIL import Image
    image = Image.open(instance.screenshot)
    image.thumbnail([300, 200], Image.ANTIALIAS)
    image.save(settings.MEDIA_ROOT + '/' + instance.screenshot.name)
    

@receiver(pre_delete, sender=Website)
def pre_delete_handler(sender, instance, using, **kwargs):
    try:
        path = settings.MEDIA_ROOT + '/' + instance.screenshot.name
        os.remove(path)
    except OSError:
        pass

pre_delete.connect(pre_delete_handler, sender=Website)
post_save.connect(post_save_handler, sender=Website)


class EditionWebsite(models.Model):
    edition = models.ForeignKey(Edition)
    website = models.ForeignKey(Website)
    help_text = "Edition specific title, if left empty, generic title is used"
    title = models.CharField(max_length=50, null=True, blank=True, help_text=help_text)
    help_text = "Edition specific description"
    desc = models.TextField(help_text=help_text)
    help_text = "Numeric value for website order. Tip: Use 100-200-300-... steps for easy reordering."
    order = models.IntegerField(help_text=help_text)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    
    
    def get_title(self):
        if self.title:
            return self.title
        else:
            return self.website.title
