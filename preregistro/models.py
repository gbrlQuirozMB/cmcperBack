from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class Medico(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualzado_en = models.DateTimeField(auto_now=True)
    # pantalla 2
    nombre = models.CharField(max_length=100)
    apPaterno = models.CharField(max_length=100, db_column='ap_paterno')
    apMaterno = models.CharField(max_length=100, db_column='ap_materno')
    rfc = models.CharField(max_length=15)
    curp = models.CharField(max_length=20)
    fechaNac = models.DateField(db_column='fecha_nacimiento')
    sexo = models.CharField(max_length=5, choices=(
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ), default="---")
    # pantalla 3
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    deleMuni = models.CharField(max_length=100, db_column='delegacion_municipio')
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    numInterior = models.CharField(max_length=10, blank=True, db_column='num_interior')
    numExterior = models.CharField(max_length=10, db_column='num_exterior')
    # pantalla 4
    rfcFacturacion = models.CharField(max_length=15, db_column='rfc_facturacion')
    usoCfdi = models.CharField(max_length=5, db_column='uso_cfdi', choices=(
        ('G03', 'Gastos en General'),
        # ('G01','Adquisición de Mercancías'),
        ('P01', 'Por Definir')
    ), default="P01")
    razonSocial = models.CharField(max_length=250, blank=True, db_column='razon_social')
    # pantalla 5.1
    paisConsult = models.CharField(max_length=100, blank=True, db_column='pais_consult')
    estadoConsult = models.CharField(max_length=100, blank=True, db_column='estado_consult')
    ciudadConsult = models.CharField(max_length=100, blank=True, db_column='ciudad_consult')
    deleMuniConsult = models.CharField(max_length=100, blank=True, db_column='delegacion_municipio_consult')
    coloniaConsult = models.CharField(max_length=100, blank=True, db_column='colonia_consult')
    calleConsult = models.CharField(max_length=100, blank=True, db_column='calle_consult')
    cpConsult = models.CharField(max_length=10, blank=True, db_column='cp_consult')
    numInteriorConsult = models.CharField(max_length=10, blank=True, db_column='num_interior_consult')
    numExteriorConsult = models.CharField(max_length=10, blank=True, db_column='num_exterior_consult')
    # pantalla 6
    cedProfesional = models.CharField(max_length=20, db_column='ced_profesional')
    cedEspecialidad = models.CharField(max_length=20, db_column='ced_especialidad')
    cedCirugiaGral = models.CharField(max_length=20, db_column='ced_cirugia_gral')
    hospitalResi = models.CharField(max_length=150, db_column='hospital_residencia')
    telJefEnse = models.CharField(max_length=15, db_column='tel_jefatura_ense')
    fechaInicioResi = models.DateField(db_column='fecha_inicio_residencia')
    fechaFinResi = models.DateField(db_column='fecha_fin_residencia')
    # pantalla 7
    telCelular = models.CharField(max_length=15, db_column='tel_celular')
    telParticular = models.CharField(max_length=15, db_column='tel_particular')
    telConsultorio = models.CharField(max_length=15, blank=True, db_column='tel_consultorio')
    email = models.CharField(max_length=50)
    emailAlterno = models.CharField(max_length=50, blank=True, db_column='email_alterno')
    # historia-2 doc-1 pantalla-4
    isExtranjero = models.BooleanField(default=False, db_column='is_extranjero')
    nacionalidad = models.CharField(max_length=100, blank=True)
    # historia-2 doc-1 pantalla-5
    estudioExtranjero = models.BooleanField(default=False, db_column='estudio_extranjero')
    escuelaExtranjero = models.CharField(max_length=200, blank=True, db_column='escuela_extranjero')
    # administracion interna
    aceptado = models.BooleanField(default=False)
    motivo = models.TextField(blank=True)
    numRegistro = models.IntegerField(blank=True, null=True, db_column='num_registro')
    username = models.CharField(max_length=150, blank=True)
    fotoPerfil = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])], db_column='foto_perfil', upload_to='preregistro')
    # agregando por mas cosas solicitadas redes sociales
    instagram = models.CharField(max_length=300, blank=True)
    facebook = models.CharField(max_length=300, blank=True)
    twitter = models.CharField(max_length=300, blank=True)
    whatsapp = models.CharField(max_length=300, blank=True)
    linkedin = models.CharField(max_length=300, blank=True)
    pagWeb = models.CharField(max_length=300, blank=True, db_column='pag_web')
    # mas cambios solicitados
    telConsultorioPublico = models.CharField(max_length=15, blank=True, db_column='tel_consultorio_publico')
    telCelularPublico = models.CharField(max_length=15, blank=True, db_column='tel_celular_publico')

    class Meta:
        db_table = 'pre_registro_medico'
        ordering = ['-creado_en']


class HorarioAtencion(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoHA')
    dia = models.CharField(max_length=15, choices=(
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ))
    horaInicio = models.CharField(max_length=10, blank=True, db_column='hora_inicio')
    horaTermino = models.CharField(max_length=10, blank=True, db_column='hora_termino')

    class Meta:
        db_table = 'horario_atencion'
        ordering = ['-medico']
