from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import RehabCenter, TreatmentType, Amenity
from .serializers import (
    RehabCenterListSerializer,
    RehabCenterDetailSerializer,
    TreatmentTypeSerializer,
    AmenitySerializer,
)


class RehabCenterListView(generics.ListAPIView):
    serializer_class = RehabCenterListSerializer

    def get_queryset(self):
        queryset = RehabCenter.objects.all()

        pk = self.request.query_params.get('pk')
        if pk:
            queryset = queryset.filter(pk=pk)

        # Search
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(city__icontains=query) |
                Q(address__icontains=query)
            )

        # Treatment filter — fixed: outside the if query block
        treatment = self.request.query_params.get('treatment')
        if treatment:
            queryset = queryset.filter(treatment_types__slug=treatment)

        price = self.request.query_params.get('price')
        if price:
            queryset = queryset.filter(price_range=price)

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(centre_type=category)

        surrounding = self.request.query_params.get('surrounding')
        if surrounding:
            queryset = queryset.filter(surroundings__contains=[surrounding])

        return queryset.distinct()

class RehabCenterByIdView(generics.RetrieveAPIView):
    serializer_class = RehabCenterListSerializer
    queryset = RehabCenter.objects.all()
    lookup_field = 'pk'
    
class RehabCenterDetailView(generics.RetrieveAPIView):
    serializer_class = RehabCenterDetailSerializer
    queryset = RehabCenter.objects.all()
    lookup_field = 'slug'


class TreatmentTypeListView(generics.ListAPIView):
    serializer_class = TreatmentTypeSerializer
    queryset = TreatmentType.objects.all()


class AmenityListView(generics.ListAPIView):
    serializer_class = AmenitySerializer
    queryset = Amenity.objects.all()


class FilterOptionsView(APIView):
    """
    GET /api/filters/
    Returns all available filter options that have at least one listing.
    Frontend uses this to show/hide filters dynamically.
    """
    permission_classes = []

    def get(self, request):
        # Treatments that have at least one center
        treatments = list(
            TreatmentType.objects.filter(centers__isnull=False)
            .distinct()
            .values('id', 'name', 'slug', 'category')
        )

        # Cities
        cities = list(
            RehabCenter.objects.exclude(city='')
            .values_list('city', flat=True)
            .distinct()
            .order_by('city')
        )

        # Surroundings — flatten JSONField list
        surroundings_qs = RehabCenter.objects.exclude(surroundings=[]).values_list('surroundings', flat=True)
        surroundings = list(set(
            s for surr_list in surroundings_qs for s in (surr_list or [])
        ))

        # Price ranges
        price_ranges = list(
            RehabCenter.objects.exclude(price_range='')
            .values_list('price_range', flat=True)
            .distinct()
        )

        # Categories
        categories = list(
            RehabCenter.objects.exclude(centre_type='')
            .values_list('centre_type', flat=True)
            .distinct()
        )

        # Languages — flatten JSONField list
        languages_qs = RehabCenter.objects.exclude(languages=[]).values_list('languages', flat=True)
        all_languages = list(set(
            lang for langs in languages_qs for lang in (langs or [])
        ))

        # Patient profiles — flatten JSONField list
        profiles_qs = RehabCenter.objects.exclude(patient_profiles=[]).values_list('patient_profiles', flat=True)
        all_profiles = list(set(
            p for profiles in profiles_qs for p in (profiles or [])
        ))

        return Response({
            'treatments': treatments,
            'cities': cities,
            'surroundings': surroundings,
            'genders': [],
            'price_ranges': price_ranges,
            'categories': categories,
            'languages': all_languages,
            'patient_profiles': all_profiles,
        })