from rest_framework import serializers
from .models import Test, Pregunta, Opcion

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'letra', 'peso']

class OpcionPublicaSerializer(serializers.ModelSerializer):
    """Sin exponer el peso al estudiante"""
    class Meta:
        model = Opcion
        fields = ['id', 'texto', 'letra']

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id', 'test', 'texto', 'area', 'orden', 'opciones']

class TestSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)
    total_preguntas = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'nombre', 'descripcion', 'activo',
                  'fecha_creacion', 'fecha_modificacion',
                  'total_preguntas', 'preguntas']

    def get_total_preguntas(self, obj):
        return obj.preguntas.count()

# ── Serializer para crear/editar test con preguntas y opciones anidadas ──

class OpcionInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    texto = serializers.CharField()
    letra = serializers.CharField(max_length=1)
    peso = serializers.IntegerField(min_value=1, max_value=4)

class PreguntaInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    texto = serializers.CharField()
    area = serializers.ChoiceField(choices=['tiempo', 'metodos', 'entorno'])
    orden = serializers.IntegerField(default=0)
    opciones = OpcionInputSerializer(many=True)

class CrearTestSerializer(serializers.ModelSerializer):
    preguntas = PreguntaInputSerializer(many=True, required=False)

    class Meta:
        model = Test
        fields = ['id', 'nombre', 'descripcion', 'activo', 'preguntas']

    def create(self, validated_data):
        preguntas_data = validated_data.pop('preguntas', [])
        test = Test.objects.create(**validated_data)
        self._guardar_preguntas(test, preguntas_data)
        return test

    def update(self, instance, validated_data):
        preguntas_data = validated_data.pop('preguntas', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if preguntas_data is not None:
            self._sincronizar_preguntas(instance, preguntas_data)
        return instance

    def _guardar_preguntas(self, test, preguntas_data):
        for p_data in preguntas_data:
            opciones_data = p_data.pop('opciones', [])
            pregunta = Pregunta.objects.create(test=test, **p_data)
            for o_data in opciones_data:
                Opcion.objects.create(pregunta=pregunta, **o_data)

    def _sincronizar_preguntas(self, test, preguntas_data):
        ids_entrantes = [p.get('id') for p in preguntas_data if p.get('id')]
        # Eliminar preguntas que ya no están
        test.preguntas.exclude(id__in=ids_entrantes).delete()

        for p_data in preguntas_data:
            opciones_data = p_data.pop('opciones', [])
            p_id = p_data.pop('id', None)

            if p_id:
                pregunta = Pregunta.objects.get(id=p_id, test=test)
                for attr, val in p_data.items():
                    setattr(pregunta, attr, val)
                pregunta.save()
            else:
                pregunta = Pregunta.objects.create(test=test, **p_data)

            # Sincronizar opciones
            ids_opciones = [o.get('id') for o in opciones_data if o.get('id')]
            pregunta.opciones.exclude(id__in=ids_opciones).delete()

            for o_data in opciones_data:
                o_id = o_data.pop('id', None)
                if o_id:
                    Opcion.objects.filter(id=o_id).update(**o_data)
                else:
                    Opcion.objects.create(pregunta=pregunta, **o_data)