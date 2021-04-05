# -*- coding: utf-8 -*-
__author__ = "María Andrea Vignau (mavignau@gmail.com)"
__copyright__ = "(C) 2016 María Andrea Vignau. GNU GPL 3."


@auth.requires_login()
def index():
    #  Get filters
    searchText = request.get_vars.searchText

    #  Build query
    query = (db.persona.created_by == auth.user.id)
    if searchText and searchText.strip() != '':
        q = (db.persona.apellido.contains(searchText))
        q |= (db.persona.nombre.contains(searchText))
        q |= (db.persona.domicilio.contains(searchText))
        q |= (db.persona.email.contains(searchText))
        query &= q
    # if len(queries) > 0:
        #query = reduce(lambda a,b:(a&b),queries)
        # constraints={'contact':query}

    # para mostrar la grilla del costado que permite navegar en los expedientes
    expte_rows = False
    if len(request.args) > 1 and request.args[0] != 'new':
        query = db.parte.persona_id == (request.args(2, cast=int))
        if db(query).select(db.parte.id):
            expte_rows = SQLFORM.grid(
                db.parte.persona_id == (
                    request.args(
                        2,
                        cast=int)),
                fields=[
                    db.parte.expediente_id,
                    db.parte.caracter],
                maxtextlength=40,
                searchable=False,
                sortable=True,
                deletable=False,
                editable=False,
                details=False,
                create=False,
                exportclasses=myexport)

    grid = SQLFORM.grid(query,
                        fields=[db.persona.apellido,
                                db.persona.nombre,
                                db.persona.domicilio,
                                db.persona.email,
                                db.persona.telefono,
                                db.persona.celular],
                        orderby=db.persona.apellido,
                        user_signature=True,
                        maxtextlength=50,
                        search_widget=contactSearch)
    return locals()


def contactSearch(self, url):
    'widget personalizado para la busqueda de personas'
    form = FORM(
        LABEL(T('Ingrese:')),
        INPUT(_name='searchText', _value=request.get_vars.searchText,
              _style='width:70%;',
              _id='searchText'),
        INPUT(_type='submit', _value=T('Search')),
        INPUT(_type='submit', _value=T('Clear'),

              _onclick="jQuery('#searchText').val('');"),
        _id='contactSearch',
        _method='GET',
        _action=url,
    )

    return form
