import Levenshtein
import streamlit as st


# Traducimos las opciones que podemos tener a numeros para escribirlas así en los informes
def convertir_numero(texto):
    conversion = {
        'Cero': 0,
        'Uno': 1,
        'Dos': 2,
        'Tres': 3,
        'Cuatro': 4,
        'Cinco': 5,
        'Seis': 6,
        'Siete': 7,
        'Ocho': 8,
        'Nueve': 9,
        'Diez': 10,
        'Once': 11,
        'Doce': 12,
        'Trece': 13,
        'Catorce': 14,
        'Quince': 15,
        'Dieciséis': 16,
        'Diecisiete': 17,
        'Dieciocho': 18,
        'Diecinueve': 19,
        'Veinte': 20,
        'Veintiuno': 21,
        'Veintidós': 22,
        'Veintitrés': 23,
        'Veinticuatro': 24,
        'Veinticinco': 25,
        'Veintiséis': 26,
        'Veintisiete': 27,
        'Veintiocho': 28,
        'Veintinueve': 29,
        'Treinta': 30,
        'Treinta y uno': 31,
        'Treinta y dos': 32,
        'Treinta y tres': 33,
        'Treinta y cuatro': 34,
        'Treinta y cinco': 35,
        'Treinta y seis': 36,
        'Treinta y siete': 37,
        'Treinta y ocho': 38,
        'Treinta y nueve': 39,
        'Cuarenta': 40,
        'Cuarenta y uno': 41,
        'Cuarenta y dos': 42,
        'Cuarenta y tres': 43,
        'Cuarenta y cuatro': 44,
        'Cuarenta y cinco': 45,
        'Cuarenta y seis': 46,
        'Cuarenta y siete': 47,
        'Cuarenta y ocho': 48,
        'Cuarenta y nueve': 49,
        'Cincuenta': 50,
        'Cincuenta y uno': 51,
        'Cincuenta y dos': 52,
        'Cincuenta y tres': 53,
        'Cincuenta y cuatro': 54,
        'Cincuenta y cinco': 55,
        'Cincuenta y seis': 56,
        'Cincuenta y siete': 57,
        'Cincuenta y ocho': 58,
        'Cincuenta y nueve': 59,
        'Sesenta': 60,
        'Sesenta y uno': 61,
        'Sesenta y dos': 62,
        'Sesenta y tres': 63,
        'Sesenta y cuatro': 64,
        'Sesenta y cinco': 65,
        'Sesenta y seis': 66,
        'Sesenta y siete': 67,
        'Sesenta y ocho': 68,
        'Sesenta y nueve': 69,
        'Setenta': 70,
        'Setenta y uno': 71,
        'Setenta y dos': 72,
        'Setenta y tres': 73,
        'Setenta y cuatro': 74,
        'Setenta y cinco': 75,
        'Setenta y seis': 76,
        'Setenta y siete': 77,
        'Setenta y ocho': 78,
        'Setenta y nueve': 79,
        'Ochenta': 80,
        'Ochenta y uno': 81,
        'Ochenta y dos': 82,
        'Ochenta y tres': 83,
        'Ochenta y cuatro': 84,
        'Ochenta y cinco': 85,
        'Ochenta y seis': 86,
        'Ochenta y siete': 87,
        'Ochenta y ocho': 88,
        'Ochenta y nueve': 89,
        'Noventa': 90,
        'Noventa y uno': 91,
        'Noventa y dos': 92,
        'Noventa y tres': 93,
        'Noventa y cuatro': 94,
        'Noventa y cinco': 95,
        'Noventa y seis': 96,
        'Noventa y siete': 97,
        'Noventa y ocho': 98,
        'Noventa y nueve': 99,
        'Cien': 100
    }
    
    traduccion = {
        'Nunca': 0,
        'Casi nunca': 1,
        'Algunas veces': 2,
        'Casi siempre': 3,
        'Siempre': 4,
    }

    if texto in conversion:
        return conversion[texto]
    elif texto in traduccion:
        return traduccion[texto]
    else:
        return None 
    
# Buscamos la opcion más similar de lo que se entiende entre la lista de las opciones posibles
def encontrar_similar(texto, opciones):
    mas_parecido = float('inf')
    elegida = None
    for opcion in opciones:
        similitud = Levenshtein.distance(texto, opcion)
        if similitud < mas_parecido:
            mas_parecido = similitud
            elegida = opcion
    return elegida

# Comprobamos que es un numero escrito con letra o con dígitos
def es_numero(value):
    if value.isdigit() == False: value = convertir_numero(value)
    if value != None: valido = True
    else: valido = False
    return value,valido