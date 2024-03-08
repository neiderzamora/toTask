#Files
from .serializers import *
from base.models import Activities
from users.models import CustomUser
from subActivities.models import SubActivities
from tasks.models import Task
from base.utils import *

#Rest_framework
from rest_framework import serializers
from django.core.exceptions import ValidationError

def validate_duplicate_data(serializer_class, data):
    date_start = data.get('date_start')
    date_finish = data.get('date_finish')
    name = data.get('name')
    description = data.get('description')
    percentage = data.get('percentage')

    existing_data = serializer_class.Meta.model.objects.filter(
        date_start=date_start,
        date_finish=date_finish,
        description=description,
        percentage=percentage,
        name=name
    ).first()

    if existing_data:
        raise serializers.ValidationError("Error, no es posible ingresar información duplicada")

class BaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(format='%Y-%m-%e %H:%M', read_only=True)
    date_start = serializers.DateTimeField(format='%Y-%m-%e %H:%M')
    date_finish = serializers.DateTimeField(format='%Y-%m-%e %H:%M')
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all()
    )

    name = serializers.CharField(error_messages={
        'blank': 'Por favor, ingrese un nombre.'
    })
    description = serializers.CharField(error_messages={
        'blank': 'Por favor, ingrese una descripcion.'
    })
    assigned_resources = serializers.CharField(error_messages={
        'blank': 'Por favor, ingrese los recursos asignados.'
    })

    class Meta:
        abstract = True

class TaskSerializer(BaseSerializer):
    proof = serializers.SerializerMethodField()
    user_staff = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all()
    )    
    subActivity = serializers.SlugRelatedField(
        slug_field="name",
        queryset=SubActivities.objects.all()
    )

    class Meta(BaseSerializer.Meta):
        model = Task
        fields = '__all__'
        read_only_fields = ['id', 'date_created']
    
    def validate(self, data):
        validate_duplicate_data(TaskSerializer, data)
        return data

    def validate_percentage(self, value):
        if value > 1.0 or value <= 0.0:
            raise serializers.ValidationError("El porcentaje no puede ser superior al 100% ni menor al 0%.")
        return value
    
    def get_proof(self, obj):
        return "def example"

    def create(self, validated_data):
        subActivity = validated_data.get('subActivity')
        percentage = validated_data.get('percentage')
        
        if subActivity:
            tasks = Task.objects.filter(subActivity=subActivity)
            total_percentage = sum(task.percentage for task in tasks) + percentage
            if total_percentage > 1.0:
                raise serializers.ValidationError({"non_field_errors": ["La suma de los porcentajes de tareas para esta subactividad no puede exceder el 100%."]})

        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        subActivity = validated_data.get('subActivity', instance.subActivity)
        percentage = validated_data.get('percentage', instance.percentage)
        
        if subActivity:
            tasks = Task.objects.filter(subActivity=subActivity).exclude(id=instance.id)
            total_percentage = sum(task.percentage for task in tasks) + percentage
            if total_percentage > 1.0:
                raise serializers.ValidationError({"non_field_errors": ["La suma de los porcentajes de tareas para esta subactividad no puede exceder el 100%."]})

        instance.name = validated_data.get('name', instance.name)
        instance.percentage = percentage
        instance.subActivity = subActivity
        instance.save()
        return instance

class SubActivitySerializer(BaseSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    overall_percentage = serializers.SerializerMethodField()
    activity = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Activities.objects.all()
    )

    class Meta(BaseSerializer.Meta):
        model = SubActivities
        fields = '__all__'
        read_only_fields = ['id', 'date_created']

    def validate(self, data):
        validate_duplicate_data(SubActivitySerializer, data)
        return data
    
    def get_overall_percentage(self, obj):
        approved_percentages = [task.percentage for task in obj.tasks.filter(status='Aprovada')]
        total_percentage = sum(approved_percentages)
        
        return total_percentage

    def validate(self, data):
        total_percentage = sum(task.get('percentage', 0) for task in data.get('tasks', []))

        if total_percentage > 100:
            raise serializers.ValidationError({"non_field_errors": ["The sum of task percentages cannot exceed 100%."]})

        return data
    
    def validate_percentage(self, value):
        if value > 1.0 or value <= 0.0:
            raise serializers.ValidationError("El porcentaje no puede ser superior al 100% ni menor al 0%.")
        return value

    def create(self, validated_data):
        activity = validated_data.get('activity')
        percentage = validated_data.get('percentage')
        
        if activity:
            subactities = SubActivities.objects.filter(activity=activity)
            total_percentage = sum(task.percentage for task in subactities) + percentage
            if total_percentage > 1.0:
                raise serializers.ValidationError({"non_field_errors": ["La suma de los porcentajes de las sub-actividades para esta actividad no puede exceder el 100%."]})

        return SubActivities.objects.create(**validated_data)

    def update(self, instance, validated_data):
        activity = validated_data.get('activity', instance.activity)
        percentage = validated_data.get('percentage', instance.percentage)
        
        if activity:
            subactities = SubActivities.objects.filter(activity=activity).exclude(id=instance.id)
            total_percentage = sum(task.percentage for task in subactities) + percentage
            if total_percentage > 1.0:
                raise serializers.ValidationError({"non_field_errors": ["La suma de los porcentajes de las sub-actividades para esta actividad no puede exceder el 100%."]})

        instance.name = validated_data.get('name', instance.name)
        instance.percentage = percentage
        instance.activity = activity
        instance.save()
        return instance        

class ActivitySerializer(BaseSerializer):
    subactivities = SubActivitySerializer(many=True, read_only=True)
    overall_percentage = serializers.SerializerMethodField()
    subactivities = SubActivitySerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        model = Activities
        fields = '__all__'
        read_only_fields = ['id', 'date_created']

    def validate(self, data):
        validate_duplicate_data(ActivitySerializer, data)
        return data

    def get_overall_percentage(self, obj):
        approved_percentages = [subactivities.percentage for subactivities in obj.subactivities.filter(status='Aprovada')]
        total_percentage = sum(approved_percentages)
        
        return total_percentage
