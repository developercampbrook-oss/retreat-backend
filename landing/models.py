from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from modelcluster.fields import ParentalKey


CONTENT_STREAMFIELD_BLOCKS = [
    ('rich_text', blocks.RichTextBlock()),
]


class FAQItem(models.Model):
    page = ParentalKey(
        'wagtailcore.Page',
        related_name='faqs',
        on_delete=models.CASCADE,
        null=True,
    )
    question = models.CharField(max_length=500)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class CityLandingPage(Page):

    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    default_city = models.CharField(max_length=100, blank=True)
    intro = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    about = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    seo_title_override = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(max_length=300, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading='Hero Section'),
        FieldPanel('default_city'),
        FieldPanel('intro'),
        FieldPanel('about'),
        InlinePanel('city_faqs', label='FAQs'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('seo_title_override'),
        FieldPanel('seo_description'),
    ]

    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('default_city'),
        APIField('intro'),
        APIField('about'),
        APIField('seo_title_override'),
        APIField('seo_description'),
        APIField('city_faqs'),
    ]

    class Meta:
        verbose_name = 'City Landing Page'

    def get_context(self, request):
        context = super().get_context(request)
        context['default_city'] = self.default_city
        context['faqs'] = self.city_faqs.all()
        return context


class CityFAQItem(models.Model):
    page = ParentalKey(
        CityLandingPage,
        related_name='city_faqs',
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length=500)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class TreatmentLandingPage(Page):

    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField(blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    default_treatment_slug = models.CharField(max_length=100, blank=True)
    intro = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    about = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    seo_title_override = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(max_length=300, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_image'),
        ], heading='Hero Section'),
        FieldPanel('default_treatment_slug'),
        FieldPanel('intro'),
        FieldPanel('about'),
        InlinePanel('treatment_faqs', label='FAQs'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('seo_title_override'),
        FieldPanel('seo_description'),
    ]

    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('default_treatment_slug'),
        APIField('intro'),
        APIField('about'),
        APIField('seo_title_override'),
        APIField('seo_description'),
        APIField('treatment_faqs'),
    ]

    class Meta:
        verbose_name = 'Treatment Landing Page'


class TreatmentFAQItem(models.Model):
    page = ParentalKey(
        TreatmentLandingPage,
        related_name='treatment_faqs',
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length=500)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question


class SEOLandingPage(Page):

    # Hero Section
    hero_title = models.CharField(max_length=255)
    hero_subtitle = models.TextField(blank=True)
    hero_left_text = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True, help_text='Content shown on left side of hero')
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Image shown on right side of hero'
    )
    hero_badge_1 = models.CharField(max_length=100, blank=True, help_text='e.g. Expert Reviewed')
    hero_badge_2 = models.CharField(max_length=100, blank=True, help_text='e.g. Updated for 2026')
    hero_badge_3 = models.CharField(max_length=100, blank=True, help_text='e.g. Verified Information')
    hero_badge_4 = models.CharField(max_length=100, blank=True, help_text='e.g. 100% Confidential')

    # Intro Section
    intro_text = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)

    # Content Sections
    section_1_title = models.CharField(max_length=255, blank=True)
    section_1_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    section_2_title = models.CharField(max_length=255, blank=True)
    section_2_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    section_3_title = models.CharField(max_length=255, blank=True)
    section_3_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    section_4_title = models.CharField(max_length=255, blank=True)
    section_4_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    section_5_title = models.CharField(max_length=255, blank=True)
    section_5_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)

    # Rehab Listings
    listing_section_title = models.CharField(max_length=255, default='Top Rehabs')
    selected_rehab_ids = models.JSONField(
        default=list,
        blank=True,
        help_text='List of RehabCenter IDs e.g. [1, 2, 3]'
    )

    # Bottom Content Sections
    bottom_section_1_title = models.CharField(max_length=255, blank=True)
    bottom_section_1_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    bottom_section_2_title = models.CharField(max_length=255, blank=True)
    bottom_section_2_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)
    bottom_section_3_title = models.CharField(max_length=255, blank=True)
    bottom_section_3_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)

    # Final CTA
    final_thoughts_title = models.CharField(max_length=255, blank=True)
    final_thoughts_content = StreamField(CONTENT_STREAMFIELD_BLOCKS, blank=True)

    # SEO
    seo_title_override = models.CharField(max_length=255, blank=True)
    seo_description = models.TextField(max_length=300, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_left_text'),
            FieldPanel('hero_image'),
            FieldPanel('hero_badge_1'),
            FieldPanel('hero_badge_2'),
            FieldPanel('hero_badge_3'),
            FieldPanel('hero_badge_4'),
        ], heading='Hero Section'),
        FieldPanel('intro_text'),
        MultiFieldPanel([
            FieldPanel('section_1_title'),
            FieldPanel('section_1_content'),
        ], heading='Content Section 1'),
        MultiFieldPanel([
            FieldPanel('section_2_title'),
            FieldPanel('section_2_content'),
        ], heading='Content Section 2'),
        MultiFieldPanel([
            FieldPanel('section_3_title'),
            FieldPanel('section_3_content'),
        ], heading='Content Section 3'),
        MultiFieldPanel([
            FieldPanel('section_4_title'),
            FieldPanel('section_4_content'),
        ], heading='Content Section 4'),
        MultiFieldPanel([
            FieldPanel('section_5_title'),
            FieldPanel('section_5_content'),
        ], heading='Content Section 5'),
        MultiFieldPanel([
            FieldPanel('listing_section_title'),
            FieldPanel('selected_rehab_ids'),
        ], heading='Rehab Listings'),
        MultiFieldPanel([
            FieldPanel('bottom_section_1_title'),
            FieldPanel('bottom_section_1_content'),
        ], heading='Bottom Section 1'),
        MultiFieldPanel([
            FieldPanel('bottom_section_2_title'),
            FieldPanel('bottom_section_2_content'),
        ], heading='Bottom Section 2'),
        MultiFieldPanel([
            FieldPanel('bottom_section_3_title'),
            FieldPanel('bottom_section_3_content'),
        ], heading='Bottom Section 3'),
        MultiFieldPanel([
            FieldPanel('final_thoughts_title'),
            FieldPanel('final_thoughts_content'),
        ], heading='Final Thoughts'),
        InlinePanel('seo_faqs', label='FAQs'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('seo_title_override'),
        FieldPanel('seo_description'),
    ]

    api_fields = [
        APIField('hero_title'),
        APIField('hero_subtitle'),
        APIField('hero_left_text'),
        APIField('hero_image', serializer=ImageRenditionField('fill-800x600')),
        APIField('hero_badge_1'),
        APIField('hero_badge_2'),
        APIField('hero_badge_3'),
        APIField('hero_badge_4'),
        APIField('intro_text'),
        APIField('section_1_title'),
        APIField('section_1_content'),
        APIField('section_2_title'),
        APIField('section_2_content'),
        APIField('section_3_title'),
        APIField('section_3_content'),
        APIField('section_4_title'),
        APIField('section_4_content'),
        APIField('section_5_title'),
        APIField('section_5_content'),
        APIField('listing_section_title'),
        APIField('selected_rehab_ids'),
        APIField('bottom_section_1_title'),
        APIField('bottom_section_1_content'),
        APIField('bottom_section_2_title'),
        APIField('bottom_section_2_content'),
        APIField('bottom_section_3_title'),
        APIField('bottom_section_3_content'),
        APIField('final_thoughts_title'),
        APIField('final_thoughts_content'),
        APIField('seo_faqs'),
        APIField('seo_title_override'),
        APIField('seo_description'),
    ]

    class Meta:
        verbose_name = 'SEO Landing Page'


class SEOLandingFAQ(models.Model):
    page = ParentalKey(
        SEOLandingPage,
        related_name='seo_faqs',
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length=500)
    answer = RichTextField()
    order = models.PositiveIntegerField(default=0)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
        FieldPanel('order'),
    ]

    api_fields = [
        APIField('question'),
        APIField('answer'),
        APIField('order'),
    ]
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question