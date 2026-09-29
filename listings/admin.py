from django import forms
from django.contrib import admin
from .models import (
    RehabCenter, TreatmentType, Amenity,
    RehabCenterPhoto, RehabCenterTeamMember, RehabCenterAboutSection,
    SURROUNDING_CHOICES, TREATMENT_CHOICES, PATIENT_PROFILE_CHOICES,
    MAIN_FACILITIES_CHOICES, IN_ROOM_FACILITIES_CHOICES,
    CENTER_FACILITIES_CHOICES, ACTIVITIES_CHOICES, LANGUAGE_CHOICES,
)


class MultiCheckboxWidget(forms.CheckboxSelectMultiple):
    pass


class MultiCheckboxField(forms.MultipleChoiceField):
    widget = MultiCheckboxWidget


class RehabCenterAdminForm(forms.ModelForm):
    languages = MultiCheckboxField(choices=LANGUAGE_CHOICES, required=False)
    surroundings = MultiCheckboxField(choices=SURROUNDING_CHOICES, required=False)
    treatments = MultiCheckboxField(choices=TREATMENT_CHOICES, required=False)
    patient_profiles = MultiCheckboxField(choices=PATIENT_PROFILE_CHOICES, required=False)
    main_facilities = MultiCheckboxField(choices=MAIN_FACILITIES_CHOICES, required=False)
    in_room_facilities = MultiCheckboxField(choices=IN_ROOM_FACILITIES_CHOICES, required=False)
    center_facilities = MultiCheckboxField(choices=CENTER_FACILITIES_CHOICES, required=False)
    activities = MultiCheckboxField(choices=ACTIVITIES_CHOICES, required=False)
    treatment_types = forms.ModelMultipleChoiceField(  # ← add this
        queryset=TreatmentType.objects.all().order_by('category', 'name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Treatment Types'
    )

    class Meta:
        model = RehabCenter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate checkboxes from JSON fields
        instance = kwargs.get('instance')
        if instance:
            for field in ['languages', 'surroundings', 'treatments', 'patient_profiles',
                          'main_facilities', 'in_room_facilities', 'center_facilities', 'activities']:
                self.initial[field] = getattr(instance, field, [])

    def clean_languages(self):
        return self.cleaned_data.get('languages', [])

    def clean_surroundings(self):
        return self.cleaned_data.get('surroundings', [])

    def clean_treatments(self):
        return self.cleaned_data.get('treatments', [])

    def clean_patient_profiles(self):
        return self.cleaned_data.get('patient_profiles', [])

    def clean_main_facilities(self):
        return self.cleaned_data.get('main_facilities', [])

    def clean_in_room_facilities(self):
        return self.cleaned_data.get('in_room_facilities', [])

    def clean_center_facilities(self):
        return self.cleaned_data.get('center_facilities', [])

    def clean_activities(self):
        return self.cleaned_data.get('activities', [])


class PhotoInline(admin.TabularInline):
    model = RehabCenterPhoto
    extra = 1


class TeamMemberInline(admin.TabularInline):
    model = RehabCenterTeamMember
    extra = 1


class AboutSectionInline(admin.TabularInline):
    model = RehabCenterAboutSection
    extra = 1


@admin.register(RehabCenter)
class RehabCenterAdmin(admin.ModelAdmin):
    form = RehabCenterAdminForm
    list_display = ['name', 'district', 'state', 'centre_type', 'price_range']
    list_filter = ['centre_type', 'price_range', 'state']
    search_fields = ['name', 'district', 'state', 'mobile', 'email']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PhotoInline, TeamMemberInline, AboutSectionInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'mobile', 'mobile_alternate', 'email', 'website', 'whatsapp')
        }),
        ('Location', {
            'fields': ('district', 'state', 'city', 'address', 'pincode', 'google_maps_url', 'lat', 'lng')
        }),
        ('Centre Details', {
            'fields': ('centre_type', 'certified_from', 'about', 'short_description')
        }),
        ('Program Details', {
            'fields': ('experience_years', 'program_duration_min', 'program_duration_max', 'occupancy', 'price_range')
        }),
        ('Languages', {
            'fields': ('languages',)
        }),
        ('Surroundings', {
            'fields': ('surroundings',)
        }),
        ('Treatments', {          # ← add this
        'fields': ('treatment_types',)
        }),
        ('Patient Profile', {
            'fields': ('patient_profiles',)
        }),
        ('Main Facilities', {
            'fields': ('main_facilities',)
        }),
        ('In-Room Facilities', {
            'fields': ('in_room_facilities',)
        }),
        ('Center Facilities', {
            'fields': ('center_facilities',)
        }),
        ('Activities', {
            'fields': ('activities',)
        }),
        ('Additional', {
            'fields': ('videos',)
        }),
        ('SEO', {
            'fields': ('seo_title', 'seo_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}