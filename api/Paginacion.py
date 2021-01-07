from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.logger import log

class Paginacion:
    totalElements = 0
    totalPages = 0

    def __init__(self, queryset, serializer, size, direc, orderby, page):
        self.queryset = queryset
        self.serializer = serializer
        self.size = size
        self.direc = direc
        self.orderby = orderby
        self.page = page

    def paginar(self):
        try:
            size = int(self.size)
            if size < 1:
                size = 10
        except:
            size = 10

        direc = str(self.direc)
        if direc.lower() == 'asc':
            direc = ''
        else:
            direc = '-'

        orderBy = self.orderby
        if orderBy is not None and orderBy != '':
            campos = self.serializer.Meta.fields
            if orderBy not in campos:
                orderBy = 'id'
            paginator = Paginator(self.queryset.order_by(direc + orderBy), size)
        else:
            paginator = Paginator(
                self.queryset.order_by(direc + 'id'), size)

        cuenta = self.queryset.count()
        Paginacion.totalElements = cuenta
        Paginacion.totalPages = paginator.num_pages
        if direc == '-':
            direc = 'desc'
        else:
            direc = 'asc'
        log.info(f'se obtienen: {cuenta} registros, registros por pagina: {size}, direccion: {direc}, ordenados por: {orderBy}')

        page = self.page
        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(paginator.num_pages)

        return self.serializer(queryset, many=True)