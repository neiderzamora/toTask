from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from tasks.models import Task
from .serializers import EvidenceSerializer
from rest_framework.permissions import IsAuthenticated

class EvidenceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        evidences = Evidence.objects.filter(user=user)
        serializer = EvidenceSerializer(evidences, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        task_id = request.data.get('task')
        description = request.data.get('description')
        status = 'enviado'  # Estado por defecto al crear

        if not task_id or not description:
            return Response({'detail': 'Faltan campos obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=task_id, user=user)
        except Task.DoesNotExist:
            return Response({'detail': 'La tarea no existe o no pertenece al usuario.'}, status=status.HTTP_404_NOT_FOUND)

        # Crear la evidencia con el serializador
        evidence_data = {
            'user': user.id,
            'task': task.id,
            'description': description,
            'status': status,
            'files': request.FILES.getlist('archivos')  # Lista de archivos
        }
        serializer = EvidenceSerializer(data=evidence_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        evidence_id = request.data.get('evidence')
        archivo = request.FILES.get('archivo')

        if not evidence_id or not archivo:
            return Response({'detail': 'Faltan campos obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            evidence = Evidence.objects.get(id=evidence_id)
        except Evidence.DoesNotExist:
            return Response({'detail': 'La evidencia no existe.'}, status=status.HTTP_404_NOT_FOUND)

        file = File(evidence=evidence, archivo=archivo)
        file.save()

        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_201_CREATED)