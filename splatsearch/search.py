# Licensed under a 3-clause BSD style license - see LICENSE.rst

#<<<<<<< HEAD
#~ SPLAT_FORM_URL = "http://www.cv.nrao.edu/php/splat/c.php"   # for direct queries with urlencoding
#=======
#~ try:
    #~ import mechanize
#~ except ImportError:
    #~ import warnings
    #~ warnings.warn("Could not import mechanize; splatalogue will not work")


#>>>>>>> upstream/master


SPLAT_FORM_URL = "http://www.cv.nrao.edu/php/splat/c_export.php"
HIT_LIMIT = 2000

"""
NB this script has a export limit of 2000 hits.
Chaning HIT_LIMIT will change this.
"""

__all__ = ['search']

import numpy as np
try:
    from astropy.table import Table
    use_astropy = True
except (ImportError):
    use_astropy = False

import numpy as _np



SPLAT_SEARCH_QUERY = ('submit=Search&chemical_name=&calcIn=&data_version=v2.0&'
    'from=203.4&to=203.42&frequency_units=GHz&energy_range_from=&energy_range_'
    'to=&energy_range_type=eu_k&tran=&no_atmospheric=no_atmospheric&no_potenti'
    'al=no_potential&no_probable=no_probable&displayLovas=displayLovas&display'
    'SLAIM=displaySLAIM&displayJPL=displayJPL&displayCDMS=displayCDMS&displayT'
    'oyaMA=displayToyaMA&displayOSU=displayOSU&displayRecomb=displayRecomb&dis'
    'playLisa=displayLisa&displayRFI=displayRFI&ls1=ls1&ls2=ls2&ls3=ls3&ls4=ls'
    '4&ls5=ls5&el1=el1&el2=el2&el3=el3&el4=el4&show_unres_qn=show_unres_qn&sho'
    'w_upper_degeneracy=show_upper_degeneracy&show_molecule_tag=show_molecule_'
    'tag&show_qn_code=show_qn_code&export_type=current&export_delimiter=colon&'
    'offset=0&limit=1000&range=on&submit=Export')

"""
sid[]=

#  Energy level display (triggered)
# 1 : Elower (cm-1)
# 2 : Elower (K)
# 3 : Eupper (cm-1)
# 4 : Eupper (K)
el1=el1
el2=el2
el3=el3
el4=el4

# Line strength display (triggered)
# 1 : CDMS/JPL Intensity
# 2 : Sij mu2
# 3 : Sij
# 4 : Aij
# 5 : Lovas/AST
ls1=ls1
ls2=ls2
ls3=ls3
ls4=ls4
ls5=ls5

# line list (triggered)
# def all on
displayRecomb=displayRecomb 
displayLovas=displayLovas
displaySLAIM=displaySLAIM
displayJPL=displayJPL
displayCDMS=displayCDMS
displayToyaMA=displayToyaMA
displayOSU=displayOSU
displayLisa=displayLisa
displayRFI=displayRFI


# data versions (choose)
# def v2.0
data_version=v2.0
or
data_version=v1.0
or
data_version=vall

# Exclude atmospheric species (triggered)
# def on
no_atmospheric=no_atmospheric

# Exclude potential interstellar species (triggered)
# def on
no_potential=no_potential

# Exclude probable interstellar species (triggered)
# def on
no_probable=no_probable

# Exclude known AST species (triggered)
# def off
known=known

# Show ONLY NRAO Recommended Freq (triggered)
# def off
include_only_nrao=include_only_nrao

# Display Unresolved quantum numbers (triggered)
# def on
show_unres_qn=show_unres_qn

# Show upper degeneracy (triggered)
# def on
show_upper_degeneracy=show_upper_degeneracy

# Display Molecule Tag (triggered)
# def on
show_molecule_tag=show_molecule_tag

# No HFS Display (triggered)
noHFS=noHFS

# Display HFS Intensity (triggered)
displayHFS=displayHFS

# Display Quantum Number Code (triggered)
show_qn_code=show_qn_code

# Display Lab Ref (triggered)
show_lovas_labref=show_lovas_labref

# Display Obs Ref (triggered)
show_lovas_obsref=show_lovas_obsref

# Display Ordered Frequency ONLY (triggered)
show_orderedfreq_only=show_orderedfreq_only

# Display NRAO Recommended Frequencies (triggered)
show_nrao_recommended=show_nrao_recommended


# transition (triggered)
tran=1-0

# frequency
from=31
to=31
frequency_units=GHz
or 
frequency_units=MHz

# line intensity lower limit (triggered)
lill_cdms_jpl=-5
or
lill_sijmu2
or
lill_aij


# Energy range (triggered)
# but if one exists, the energy_range_type must exist
energy_range_from=10
energy_range_to=500
energy_range_type=eu_k
 or
energy_range_type=el_k
or
energy_range_type=el_cm1
or
energy_range_type=eu_cm1




submit=1
"""


#~ The urllib2 module has been split across several modules in Python 3.0
#~ named urllib.request and urllib.error. The 2to3 tool will automatically adapt imports when converting your sources to 3
#~ 
#~ So you should instead be saying
#~ 
#~ from urllib.request import urlopen
#~ html = urlopen("http://www.google.com/")
#~ print(html)

# used : 
# urllib.urlencode
# urllib2.Request
# urllib2.urlopen

try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlencode
    from urllib2 import urlopen, Request
    
# and then i can just
#~ mydata = [('one','1'),('two','2')]    #The first is the var name the second is the value
#~ mydata = urlencode(mydata)
#~ path = 'http://localhost/new.php'    #the url you want to POST to
#~ req = Request(path, mydata)
#~ req.add_header("Content-type", "application/x-www-form-urlencoded")
#~ page = urlopen(req).read()
#~ print page

###############################################################################


def search( freq = [203.4, 203.42],
            fwidth = None,
            funit = 'GHz',
            linelist = ['lovas', 'slaim', 'jpl', 'cdms', 'toyama', 'osu', 'recomb', 'lisa', 'rfi'],
            efrom = None,
            eto = None,
            eunit = None,    # 'el_cm1', 'eu_cm1', 'el_k', 'eu_k'
            trans = None,
            lill = None,    # line intensity lower limits, 'cdms_jpl', 'sijmu2', 'aij'
             **settings):

        """
            
            settings:
            ----------

            version : 2.0, 1.0, all
        """

        # prepare some of the input
        # lowercase insensitive input.
        if type(linelist) == type([]):
            linelist = [i.lower() for i in linelist]
        else:
            lineliest = [linelist.lower()]
        
        #~ _check_input(freq, fwidth, funit, linelist, efrom, eto, eunit,
            #~ transition, lill,**settings)

        # parameters list, to be urlencoded later        
        parameters = []
        
        parameters.extend( _parameters_preamble() )
        parameters.extend( _parse_linelist( linelist ) )
        parameters.extend( _parse_settings( settings ) )
        
        parameters.extend( _parse_frequency(freq, fwidth, funit) )
        parameters.extend( _parse_linelist( linelist ) )
        
        if ((efrom is not None) or (eto is not None)):
            parameters.extend( _parse_erange( efrom, eto, eunit ) )
        if (trans is not None):
            parameters.extend( _parse_transition( trans ) )
        if (lill is not None):
            parameters.extend( _parse_lill( lill ) )
        
        parameters.extend( _parameters_ending() )
        return parameters
        results = _get_results(parameters)
        results = _parse_results(results)

        return results # temporary
        
def _parameters_preamble():
    """
        Set the default display parameters, i.e. display
        everything in the result table


        #  Energy level display (triggered)
        # 1 : Elower (cm-1)
        # 2 : Elower (K)
        # 3 : Eupper (cm-1)
        # 4 : Eupper (K)
        el1=el1
        el2=el2
        el3=el3
        el4=el4

        # Line strength display (triggered)
        # 1 : CDMS/JPL Intensity
        # 2 : Sij mu2
        # 3 : Sij
        # 4 : Aij
        # 5 : Lovas/AST
        ls1=ls1
        ls2=ls2
        ls3=ls3
        ls4=ls4
        ls5=ls5

        # Display Unresolved quantum numbers (triggered)
        # always on
        #~ show_unres_qn=show_unres_qn

        # Show upper degeneracy (triggered)
        # always on
        #~ show_upper_degeneracy=show_upper_degeneracy

        # Display Molecule Tag (triggered)
        # always on
        #~ show_molecule_tag=show_molecule_tag

        # No HFS Display (triggered)
        # not included 
        #~ noHFS=noHFS

        # Display HFS Intensity (triggered)
        # always on
        #~ displayHFS=displayHFS

        # Display Quantum Number Code (triggered)
        # always on
        #~ show_qn_code=show_qn_code

        # Display Lab Ref (triggered)
        # always off
        #~ show_lovas_labref=show_lovas_labref

        # Display Obs Ref (triggered)
        # always off
        #~ show_lovas_obsref=show_lovas_obsref

        # Display Ordered Frequency ONLY (triggered)
        #~ show_orderedfreq_only=show_orderedfreq_only

        # Display NRAO Recommended Frequencies (triggered)
        #~ show_nrao_recommended=show_nrao_recommended

        SUMMARY :
        ALWAYS ON-----------------------------------
        Display HFS Intensity  
        Display Unresolved Quantum Numbers  
        Display Upper State Degeneracy 
        Display Molecule Tag  
        Display Quantum Number Code  
        Display NRAO Recommended Frequencies
        E_levels (all)
        Line Strength Display (all)
        Display Ordered Frequency ONLY (only one frequency to parse)
        --------------------------------------------

    """
    returnlist = [
        ('submit', 'Search'),
        ('ls1','ls1'),
        ('ls2','ls2'),
        ('ls3','ls3'),
        ('ls4','ls4'),
        ('ls5','ls5'),
        ('el1', 'el1'),
        ('el2', 'el2'),
        ('el3', 'el3'),
        ('el4', 'el4'),
        ('show_unres_qn', 'show_unres_qn'),
        ('show_upper_degeneracy', 'show_upper_degeneracy'),
        ('show_molecule_tag', 'show_molecule_tag'),
        ('displayHFS', 'displayHFS'),
        ('show_qn_code', 'show_qn_code'),
        #('show_lovas_labref', 'how_lovas_labref'),          # Always OFF
        #('show_lovas_obsref', 'show_lovas_obsref'),         # Always OFF
        ('show_orderedfreq_only', 'show_orderedfreq_only'),
        ('show_nrao_recommended', 'show_nrao_recommended')
        ]
    return returnlist

def _parse_linelist(linelist):
    """
    Only search the requested line lists.
    
    # line list (triggered)
    # def all on
    displayRecomb=displayRecomb 
    displayLovas=displayLovas
    displaySLAIM=displaySLAIM
    displayJPL=displayJPL
    displayCDMS=displayCDMS
    displayToyaMA=displayToyaMA
    displayOSU=displayOSU
    displayLisa=displayLisa
    displayRFI=displayRFI
    """
    returnlist = []
    if 'lovas' in linelist:
        returnlist.append(('displayLovas'  ,'displayLovas'))
    if 'slaim' in linelist:
        returnlist.append(('displaySLAIM'  ,'displaySLAIM'))
    if 'jpl' in linelist:
        returnlist.append(('displayJPL'    ,'displayJPL'))
    if 'cdms' in linelist:
        returnlist.append(('displayCDMS'   ,'displayCDMS'))
    if 'toyama' in linelist:
        returnlist.append(('displayToyaMA' ,'displayToyaMA'))
    if 'osu' in linelist:
        returnlist.append(('displayOSU'    ,'displayOSU'))
    if 'recomb' in linelist:
        returnlist.append(('displayRecomb' ,'displayRecomb'))
    if 'lisa' in linelist:
        returnlist.append(('displayLisa'   ,'displayLisa'))
    if 'rfi' in linelist:
        returnlist.append(('displayRFI'    ,'displayRFI'))

    return returnlist

def _set_bool(settings, key, param, default):
    """
    help function to check the dictionary settings if key exsists,
    and return a on (param, param) or off (empty) tuple depending in
    settings[key] value or to the default (0:off, or 1:on ) value
    """
    if settings.has_key( key ):
        if not settings[key]:   # if its False
            return () # return empty list
        elif settings[key]: # if its True
            return (param, param)
    else: # Else we set it to the default value
        if default: # if default is On (i.e. 1)
            return (param, param)
        elif not default: # if default is Off (i.e. 0)
            return ()

def _parse_settings( settings ):
    """
    set the data release version of the splatalogue compilation

    # data versions (choose)
    # def v2.0
    data_version=v2.0
    or
    data_version=v1.0
    or
    data_version=vall
    """
    returnlist = []
    
    # Data release version
    # first parese the input
    # def v2.0
    if settings.has_key( 'version' ):
        version = settings['version']
    else:
        version = '2.0'
    # now set the parameter
    # def v2.0
    if str(version) in ['2.0', '2', '2.']:
        returnlist.append(('data_version', 'v2.0'))
    elif str(version) in ['1.0', '1', '1.']:
        returnlist.append(('data_version', 'v1.0'))
    elif str(version).lower() in ['all', 'al', 'a']:
        returnlist.append(('data_version', 'vall'))
    else:
        returnlist.append(('data_version', 'vall'))
    # Frequency error limit
    # def off
    # fel=fel
    key = 'felim'
    param = 'fel'
    default = 0
    returnlist.append( _set_bool(settings, key, param, default) )
    # Exclude atmospheric species (triggered)
    # def on
    # no_atmospheric=no_atmospheric
    key = 'no_atm'
    param = 'no_atmospheric'
    default = 1
    returnlist.append( _set_bool(settings, key, param, default) )
    # Show ONLY NRAO Recommended Freq (triggered)
    # def off
    #~ include_only_nrao=include_only_nrao
    key = 'nrao'
    param = 'include_only_nrao'
    default = 0
    returnlist.append( _set_bool(settings, key, param, default) )
    # Exclude potential interstellar species (triggered)
    # def on
    #~ no_potential=no_potential
    key = 'potential'
    param = 'no_potential'
    default = 1
    returnlist.append( _set_bool(settings, key, param, default) )
    # Exclude probable interstellar species (triggered)
    # def on
    #~ no_probable=no_probable
    key = 'probable'
    param = 'no_probable'
    default = 1
    returnlist.append( _set_bool(settings, key, param, default) )
    # Exclude known AST species (triggered)
    # def off
    #~ known=known
    key = 'known'
    param = 'known'
    default = 0
    returnlist.append( _set_bool(settings, key, param, default) )

    return returnlist

def _parse_frequency(freq, fwidth, funit):
    """
        # frequency
        from=31
        to=31
        frequency_units=GHz
        or 
        frequency_units=MHz
    """
    returnlist = []
    #### FREQUENCY
    # Two casees:
    #   1. A list with length two
    #   2. A integer/float
    if type(freq) == str:
        raise(Exception, 'Wrong format for frequency. Need list or float')
    # First guess : a list of floats with length two
    try:
        returnlist.append( ('from', str(freq[0])) )
        returnlist.append( ('to', str(freq[1])) ) 
    except (IndexError, TypeError):
        # If not a list, should be a float, and fwidth given
        try:
            freq = float(freq)
        except (ValueError):
            raise (Exception, 'Wrong format for frequency. Need list or float')
        if fwidth not in [0, 0.0, None]:
            # with freq and fwidth given, we can calculate start and end
            f1, f2 = freq + _np.array([-1,1]) * fwidth / 2.
            returnlist.append( ('from',  str(f1)) ) 
            returnlist.append( ('to',  str(f2)) )
        else:
            # the fwidth parameter is missing
            raise (Exception, 'The fwidth parameter is missing. '
            'Frequency parameter(s) malformed')
    #### FREQUENCY UNIT
    #
    if funit not in [0, None]:
        if funit.lower() in ['ghz', 'mhz']:
            returnlist.append( ('frequency_units', funit) )
        else:
            print 'Allowed frequency units : \'GHz\' or \'MHz\''
    elif not funit in [0, None]:
        funit = 'GHz'
        returnlist.append( ('frequency_units', 'GHz') )
    return returnlist

def _parse_erange( efrom, eto, eunit ):
    """
        # Energy range (triggered)
        # but if one exists, the energy_range_type must exist
        energy_range_from=10
        energy_range_to=500
        energy_range_type=eu_k
         or
        energy_range_type=el_k
        or
        energy_range_type=el_cm1
        or
        energy_range_type=eu_cm1

    """
    
    returnlist = []
    ### Energy Range
    # form['energy_range_from/to'] is a text field in the form
    # while it is called e_from/to in the function
    
    if efrom == None and eto == None and eunit != None:
        print 'You gave the Enery range type keyword, but no energy range...'
        raise Exception('energy range keywords malformed')
    #~ if (efrom not None) or (eto not None):
    eunit_ref = ['el_cm1', 'eu_cm1', 'el_k', 'eu_k']
        # check that unit is given, and correct
        # or set default (eu_k)
    # set efrom if supplied
    if efrom != None:
        returnlist.append( ('energy_range_from', str(efrom)) )
    # set eto if supplied
    if eto != None:
        returnlist.append( ('energy_range_to',  str(eto)) )
    # check if eunit is given, and tick the corresponding radio
    # button, if none then assume Kelvin
    if eunit != None: #arg.has_key('efrom') or arg.has_key('eto'):
        if eunit.lower() in eunit_ref:
            pass
        else:
            print 'Energy range unit keyword \'eunit\' malformed.'
            raise Exception('eunit keyword malformed')
    else:
        # no value, assuming its in Kelvin (i.e. Eu/kb)
        eunit = 'eu_k'
    # now set the eunit radio button
    returnlist.append( ('energy_range_type', eunit.lower() ) )   
    return returnlist

def _parse_transition( trans ):
    """
        # transition (triggered)
        tran=1-0
    """
    return ('tran', str(trans))
    
def _parse_lill( lill ):
    """
        # line intensity lower limit (triggered)
        #~ lill_cdms_jpl=-5
        #~ or
        #~ lill_sijmu2
        #~ or
        #~ lill_aij
    """
    
    ### Line Intensity Lower Limits
    if lill != None:
        if lill[1].lower() == 'cdms_jpl':
            return ( 'lill_cdms_jpl', str(lill[0]) )
        elif lill[1].lower() == 'sijmu2':
            return ( 'lill_sijmu2', str(lill[0]) )
        elif lill[1].lower() == 'aij':
            return ( 'lill_aij', str(lill[0]) )

def _parameters_ending():

    returnlist = [
    ('export_type','current'),
    ('export_delimiter','colon'),
    ('offset','0'),
    ('limit', str(HIT_LIMIT)),
    ('range','on'),
    ('submit','Export')
    ]
    return returnlist

def _get_results(parameters):
    
    parameters = urlencode(parameters)
    path = SPLAT_FORM_URL  
    req = Request(path, mydata)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    results = urlopen(req).read()
    return results

def _parse_result(data, output='astropy.table'):
    """
    Only one output type at the moment    
    """
    #TODO : what if results are empty
    if output == 'astropy.table':
        if not use_astropy:
            #~ print('Astropy not installed, try other output format')
            raise(ImportError('Astropy not installed, try other output format'))
        # get each line (i.e. each molecule)
        rows = data.split('\n')
        # get the names of the columns
        column_names = rows[0]
        column_names = column_names.split(':')
        
        for i in np.arange(len(column_names)):
            column_names[i] = column_names[i].replace('<br>', ' ')
            column_names[i] = column_names[i].replace('<sub>', '_')
            column_names[i] = column_names[i].replace('<sup>', '^')
            column_names[i] = column_names[i].replace('</sup>', '')
            column_names[i] = column_names[i].replace('</sub>', '')
            column_names[i] = column_names[i].replace('&#956;', 'mu')
            column_names[i] = column_names[i].replace('sid[0] is null', '')
        rows = rows[1:-1]
        rows = [i.split(':') for i in rows]
        rows = _np.array(rows)
        rows[rows == ''] = 'nan'
        
        column_dtypes = ['str', 'str', 'float', 'float', 'float' , 'float' ,
                        'str', 'str', 'float',
                        'float', 'float', 'float', 'str', 'float', 'float',
                        'float', 'float', 'float', 'float','float','str']
        column_units = [None, None, 'GHz?', 'GHz?', 'GHz?', 'GHz?', None, 
                        None, '?', 'Debye^2', '?', 'log10(Aij)', '?', 
                        'cm^-1', 'K', 'cm^-1', 'K', None, None, None, None]
        
        results = Table(data = rows , 
                        names = column_names, 
                        dtypes = column_dtypes)
        
        for i in _np.arange(len(column_units)):
            results.field(i).units = column_units[i]
        return results




###################


"""
TODO : fix consistent naming (resultform vs result_table)
TODO : improve the parsing, i.e., the astropy.table output
TODO : create pretty printing for on screen results?
TODO : improve searchable parameters e.g. molecule ID, 
       frequency error limit

What to do:

1. move the search over to only use the "request" module:
    -> Encode the search in the URL. (more messy, but they don't care)



all and only JPL:
el1=el1&el2=el2&el3=el3&el4=el4&ls1=ls1&ls2=ls2&ls3=ls3&ls4=ls4&ls5=ls5&displayJPL=displayJPL&
data_version=v2.0&no_atmospheric=no_atmospheric&no_potential=no_potential&
no_probable=no_probable&from=203.4&to=203.41&frequency_units=GHz&submit=1

all except Eup/down in cm-1 and only JPL
el2=el2&el4=el4&ls1=ls1&ls2=ls2&ls3=ls3&ls4=ls4&ls5=ls5&displayJPL=displayJPL&
data_version=v2.0&no_atmospheric=no_atmospheric&no_potential=no_potential&
no_probable=no_probable&from=203.4&to=203.41&frequency_units=GHz&submit=1


EVERYTHING selected and all limits entered:
	SQL Query:
	SELECT SQL_CALC_FOUND_ROWS line_id, frequency*1.0 as frequency, uncertainty, 
    orderedfreq, measfreq*1.0 as measfreq, measerrfreq, rel_int_HFS_Lovas, ll_id, 
    resolved_QNs, Sij, Sijmu2, Aij, intintensity, obsintensity_Lovas_NIST, 
    lower_state_energy, lower_state_energy_K, upper_state_energy, upper_state_energy_K, 
    rel_int_HFS_Lovas, obsref_Lovas_NIST, labref_Lovas_NIST, m.species_id, name, s_name, 
    chemical_name, Lovas_NRAO, `v1.0` as v1_0, `v2.0` as v2_0, quantum_numbers, 
    upper_state_degeneracy, molecule_tag, qn_code FROM main m, species s WHERE 
    m.species_id = s.species_id AND s.SPLAT_ID > 100 AND atmos != 1 AND potential 
    != 1 AND probable != 1 AND known_ast_molecules != 1 AND Lovas_NRAO = 1 AND 
    ((frequency > 0 and uncertainty <= 50) or (measfreq > 0 and measerrfreq <= 50)) 
    AND (resolved_QNs NOT LIKE '%F=%') AND m.`v2.0` = 2 AND ll_id in (10, 11, 12, 14, 
    15, 16, 17, 18, 19) AND orderedfreq>=203400 AND orderedfreq<=203410 AND 
    upper_state_energy_K>=1 AND upper_state_energy_K<=500 AND intintensity > -5 
    AND (ll_id=10 OR ll_id=12 OR ll_id=18) ORDER BY orderedfreq LIMIT 0, 500

	Request parameters:
	fel=fel&el1=el1&el2=el2&el3=el3&el4=el4&ls1=ls1&ls2=ls2&ls3=ls3&ls4=ls4&ls5=ls5&
    displayRecomb=displayRecomb&displayLovas=displayLovas&displaySLAIM=displaySLAIM&
    displayJPL=displayJPL&displayCDMS=displayCDMS&displayToyaMA=displayToyaMA&
    displayOSU=displayOSU&displayLisa=displayLisa&displayRFI=displayRFI&
    data_version=v2.0&no_atmospheric=no_atmospheric&no_potential=no_potential&
    no_probable=no_probable&known=known&include_only_nrao=include_only_nrao&
    tran=1-0&from=203.4&to=203.41&frequency_units=GHz&show_unres_qn=show_unres_qn&
    show_upper_degeneracy=show_upper_degeneracy&show_molecule_tag=show_molecule_tag&
    noHFS=noHFS&show_qn_code=show_qn_code&show_lovas_labref=show_lovas_labref&
    show_lovas_obsref=show_lovas_obsref&show_orderedfreq_only=show_orderedfreq_only&
    show_nrao_recommended=show_nrao_recommended&lill_cdms_jpl=-5&energy_range_from=1&
    energy_range_to=500&energy_range_type=eu_k&submit=1
    
	Columns:
	species,nrao_recommended,chemical_name,orderedfreq_ghz,resolved_qns,
    quantum_numbers,intintensity,Sijmu2,Sij,Aij,obsintensity_Lovas_NIST,
    lower_state_energy,lower_state_energy_K,upper_state_energy,upper_state_energy_K,
    rel_int_HFS_Lovas,upper_state_degeneracy,molecule_tag,qn_code,linelist,
    labref_Lovas_NIST,obsref_Lovas_NIST


# dont forget submit=1
t = t.split('&')
t = [i.split('=') for i in t]
t = dict(t)

payload = t

resp = requests.get("http://www.cv.nrao.edu/php/splat/c.php", params=payload)

-------------------------------------------------------------------------------
Get exported colon separated list


Export the results directly:



http://www.cv.nrao.edu/php/splat/c_export.php?
t ='submit=submit&chemical_name=&calcIn=&data_version=v2.0&from=203.4&to=203.42&frequency_units=GHz&energy_range_from=&energy_range_to=&energy_range_type=eu_k&tran=&no_atmospheric=no_atmospheric&no_potential=no_potential&no_probable=no_probable&displayLovas=displayLovas&displaySLAIM=displaySLAIM&displayJPL=displayJPL&displayCDMS=displayCDMS&displayToyaMA=displayToyaMA&displayOSU=displayOSU&displayRecomb=displayRecomb&displayLisa=displayLisa&displayRFI=displayRFI&ls1=ls1&ls2=ls2&ls3=ls3&ls4=ls4&ls5=ls5&el1=el1&el2=el2&el3=el3&el4=el4&show_unres_qn=show_unres_qn&show_upper_degeneracy=show_upper_degeneracy&show_molecule_tag=show_molecule_tag&show_qn_code=show_qn_code&export_type=current&export_delimiter=colon&offset=0&limit=69&range=on&submit=Export'

# dont forget submit=1

t = t.split('&')
t = [i.split('=') for i in t]
t = dict(t)

{'calcIn': '',
 'chemical_name': '',
 'data_version': 'v2.0',
 'displayCDMS': 'displayCDMS',
 'displayJPL': 'displayJPL',
 'displayLisa': 'displayLisa',
 'displayLovas': 'displayLovas',
 'displayOSU': 'displayOSU',
 'displayRFI': 'displayRFI',
 'displayRecomb': 'displayRecomb',
 'displaySLAIM': 'displaySLAIM',
 'displayToyaMA': 'displayToyaMA',
 'el1': 'el1',
 'el2': 'el2',
 'el3': 'el3',
 'el4': 'el4',
 'energy_range_from': '',
 'energy_range_to': '',
 'energy_range_type': 'eu_k',
 'export_delimiter': 'colon',
 'export_type': 'current',
 'frequency_units': 'GHz',
 'from': '203.4',
 'limit': '69',
 'ls1': 'ls1',
 'ls2': 'ls2',
 'ls3': 'ls3',
 'ls4': 'ls4',
 'ls5': 'ls5',
 'no_atmospheric': 'no_atmospheric',
 'no_potential': 'no_potential',
 'no_probable': 'no_probable',
 'offset': '0',
 'range': 'on',
 'show_molecule_tag': 'show_molecule_tag',
 'show_qn_code': 'show_qn_code',
 'show_unres_qn': 'show_unres_qn',
 'show_upper_degeneracy': 'show_upper_degeneracy',
 'submit': 'Export',
 'to': '203.42',
 'tran': ''}




payload = t

file_export = requests.get("http://www.cv.nrao.edu/php/splat/c_export.php?submit=submit", params=payload)

astropy_table = _parse_result(file_export.text.encode())


"""

#~ def search( freq = [203.4, 203.42],
            #~ fwidth = None,
            #~ funit = 'GHz',
            #~ linelist = ['lovas', 'slaim', 'jpl', 'cdms', 'toyama', 'osu', 'recomb', 'lisa', 'rfi'],
            #~ efrom = None,
            #~ eto = None,
            #~ eunit = None,    # 'el_cm1', 'eu_cm1', 'el_k', 'eu_k'
            #~ transition = None,
            #~ lill = None,    # line intensity lower limits, 'cdms_jpl', 'sijmu2', 'aij'
             #~ **settings):
    #~ """
    #~ 
    #~ Splatalogue.net search
    #~ 
    #~ Function to search the Splatalogue.net compilation
    #~ (http://www.splatalogue.net / http://www.cv.nrao.edu/php/splat/)
    #~ 
    #~ 
    #~ Parameters
    #~ ----------
    #~ 
    #~ freq : Frequencies to search between. Give a single frequency if 
            #~ 'fwidth' is given.
    #~ 
    #~ fwidth : Give only one frequency in 'freq' and a width in frequency
             #~ here.
    #~ 
    #~ funit : Frequency unit, 'GHz' or 'MHz'
    #~ 
    #~ linelist : list of the molecular line catalogs to use
        #~ available 
            #~ 'lovas'     - The LOVAS catalog http://
            #~ 'slaim'     - The SLAIM catalog http://
            #~ 'jpl'       - The JPL catalog http://
            #~ 'cdms'      - The CDMS catalog http://
            #~ 'toyama'    - The Toyama catalog http://
            #~ 'osu'       - The OSU catalog http://
            #~ 'recomb'    - The Recomd catalog http://
            #~ 'lisa'      - The LISA catalog http://
            #~ 'rfi'       - The RFI catalog http://
            #~ For example, give linelist = ['cdms', 'jpl'] to use only 
            #~ the CDMS and JPL catalogs.
    #~ 
    #~ efrom : Limit of the lower energy level
#~ 
    #~ eto : Upper limit of the upper energy level
#~ 
    #~ eunit : Unit of the given energy levels 
            #~ Available : 'el_cm1', 'eu_cm1', 'el_k', 'eu_k'
#~ 
    #~ transition : Transition numbers of the line as a string, 
                 #~ e.g. '1-0'
#~ 
    #~ lill : Line intensity lower limits. A list of first the 
           #~ limit and then the format [value, 'type']
           #~ Available formats : 'cdms_jpl', 'sijmu2', 'aij'
           #~ Example: lill = [-5, 'cdms_jpl'] for 
           #~ CDMS/JPL Intensity of 10^(-5)
   #~ 
   #~ Extra parameters:
   #~ transition : search (just like on Splatalogue.net) for a specific 
                #~ transition, e.g., "1-0"
   #~ 
    #~ 
    #~ Returns
    #~ -------
    #~ A astropy.table table, with column names, units and description.
    #~ 
    #~ 
    #~ Notes
    #~ -----
    #~ The naming of the columns in the results table, and the units is 
    #~ not complete. The names should be optimized and the units (at 
    #~ least some) should be taken from the input and/or results. 
    #~ So beware.
    #~ The column descriptions is not done either, so it is empty.
    #~ 
    #~ It queries splatalogue.net over http (mechanize/urllib), so don't 
    #~ write a script that queries their server too often.
    #~ 
    #~ Example
    #~ -------
    #~ In : from astroquery import splatalogue
    #~ In : results = splatalogue.search()
    #~ 
    #~ and e.g.
    #~ 
    #~ In : results['Freq-GHz'][results['Chemical Name'] == 'UNIDENTIFIED']
    #~ Out : <Column name='Freq-GHz' units='GHz?' format=None description=None> array([ 203.4127])
    #~ 
    #~ to get the frequency of the unidentified line(s)
    #~ 
    #~ (It will search between 203.4 and 203.42 GHz by default, giving
    #~ about 69 hits.)
    #~ 
    #~ 
    #~ 
    #~ """
    #~ 
    #~ # Get the form from the server
    #~ form = _get_form()
    #~ # Frequency
    #~ form = _parse_frequency(form, freq, fwidth, funit)
    #~ # Molecular species
    #~ #Get species molecular number, ordered by mass
    #~ # PLACEHOLDER for future implementation
    #~ # get the avaliable species from the form
    #~ sel_species = [i.attrs for i in form.find_control('sid[]').items]
    #~ form = _parse_molecular_species(form)
    #~ # Line list
    #~ form = _parse_linelist(form, linelist)
    #~ # Energy range
    #~ form = _parse_energy_range(form, efrom, eto, eunit)
    #~ # Specify transition
    #~ form = _parse_transition(form, settings)
    #~ # Line intensity lower limit
    #~ form = _parse_line_intensity(form, lill)
    #~ # Frequency error limit
    #~ form = _parse_frequency_error_limit(form)
    #~ # Other settings
    #~ form = _set_settings(form)
    #~ # Press search and get the result
    #~ data = _get_results(form)
    #~ # Parse the data into a astropy.table
    #~ results = _parse_result(data, output='astropy.table')
    #~ 
    #~ # at the moment just returns the results astropy.table
    #~ return results
#~ 
#~ 
#~ def _get_form():
    #~ # GET SERVER RESPONSE
    #~ try:
        #~ response = mechanize.urlopen(SPLAT_FORM_URL)
    #~ except mechanize.URLError:
        #~ raise Exception('No reponse from server : {0}'.format(SPLAT_FORM_URL))
    #~ 
    #~ # PARSE SERVER RESPONSE
    #~ forms = mechanize.ParseResponse(response, backwards_compat = False)
    #~ response.close()
    #~ 
    #~ # GET FORM
    #~ form = forms[0]
    #~ return form
#~ 
#~ def _parse_frequency(form, freq, fwidth, funit):
    #~ #### FREQUENCY
    #~ # Two casees:
    #~ #   1. A list with length two
    #~ #   2. A integer/float
    #~ if type(freq) == str:
        #~ # Format error, TypeError?
        #raise(TypeError, 'Wrong format for frequency. Need list or float')
        #~ raise(Exception, 'Wrong format for frequency. Need list or float')
    #~ # First guess : a list of floats with length two
    #~ try:
        #~ form['from'] = str(freq[0])
        #~ form['to'] = str(freq[1])
    #~ except (IndexError, TypeError):
        #~ # If not a list, should be a float, and fwidth given
        #~ try:
            #~ freq = float(freq)
        #~ except (ValueError):
            #~ raise (Exception, 'Wrong format for frequency. Need list or float')
        #~ if fwidth not in [0, 0.0, None]:
            #~ # with freq and fwidth given, we can calculate start and end
            #~ f1, f2 = freq + np.array([-1,1]) * fwidth / 2.
            #~ form['from'] = str(f1)
            #~ form['to'] = str(f2)
        #~ else:
            #~ # the fwidth parameter is missing
            #~ raise (Exception, 'The fwidth parameter is missing. '
            #~ 'Frequency parameter(s) malformed')
    #~ #### FREQUENCY UNIT
    #~ #
    #~ if funit not in [0, None]:
        #~ if funit.lower() in ['ghz', 'mhz']:
            #~ form['frequency_units'] = [funit]
        #~ else:
            #~ print 'Allowed frequency units : \'GHz\' or \'MHz\''
    #~ elif not funit in [0, None]:
        #~ funit = 'GHz'
        #~ form['frequency_units'] = ['GHz']
    #~ return form
#~ 
#~ def _parse_molecular_species(form):
    #~ return form
    #~ 
#~ def _parse_linelist(form, linelist):
    #~ #### LINE LIST
    #~ # define a reference list of names
    #~ mylinelist = ['lovas', 'slaim', 'jpl', 'cdms', 'toyama', 'osu', \
    #~ 'recomb', 'lisa', 'rfi']
    #~ # list of strings with the format that the search form wants
    #~ formcontrol_linelist = ["displayLovas", "displaySLAIM", \
    #~ "displayJPL", "displayCDMS", "displayToyaMA", "displayOSU", \
    #~ "displayRecomb", "displayLisa", "displayRFI"]
    #~ if type(linelist) == type('string'):
        #~ # if linelist is given as linelist='all'
        #~ if linelist.lower() == 'all':
            #~ # if we want to set all, just copy mylinelist
            #~ linelist = mylinelist
        #~ else:
            #~ print 'Linelist input not understood'
            #~ raise Exception('bad input : \'linelist\'')
    #~ elif type(linelist) == type(['list']):
        #~ # get all values to lower case, to accept capitals
        #~ linelist = [x.lower() for x in linelist]
    #~ else:
        #~ raise Exception('something is wrong with the linelist input/parsing')
#~ 
    #~ # now set the linelist search form
    #~ # check for every linelist, if it exists in the input linelist
    #~ for i,j in zip(mylinelist, formcontrol_linelist):
        #~ if i in linelist:
            #~ form.find_control(j).get().selected = True
        #~ else:
            #~ form.find_control(j).get().selected = False
#~ 
    #~ return form
#~ 
#~ def _parse_energy_range(form, efrom, eto, eunit):
    #~ ### Energy Range
    #~ # form['energy_range_from/to'] is a text field in the form
    #~ # while it is called e_from/to in the function
    #~ 
    #~ if efrom == None and eto == None and eunit != None:
        #~ print 'You gave the Enery range type keyword, but no energy range...'
        #~ raise Exception('energy range keywords malformed')
    #if (efrom not None) or (eto not None):
    #~ eunit_ref = ['el_cm1', 'eu_cm1', 'el_k', 'eu_k']
        #~ # check that unit is given, and correct
        #~ # or set default (eu_k)
    #~ # set efrom if supplied
    #~ if efrom != None:
        #~ form['energy_range_from'] = str(efrom)
    #~ # set eto if supplied
    #~ if eto != None:
        #~ form['energy_range_to'] = str(eto)
    #~ # check if eunit is given, and tick the corresponding radio
    #~ # button, if none then assume Kelvin
    #~ if eunit != None: #arg.has_key('efrom') or arg.has_key('eto'):
        #~ if eunit.lower() in eunit_ref:
            #~ pass
        #~ else:
            #~ print 'Energy range unit keyword \'eunit\' malformed.'
            #~ raise Exception('eunit keyword malformed')
    #~ else:
        #~ # no value, assuming its in Kelvin (i.e. Eu/kb)
        #~ eunit = 'eu_k'
    #~ # now set the eunit radio button
    #~ form.find_control('energy_range_type').toggle(eunit.lower())   
    #~ return form
#~ 
#~ def  _parse_transition(form, arg):
    #~ ### Specify Transition
    #~ #
    #~ if arg.has_key('transition'):
        #~ form['tran'] = str(arg['transition'])
    #~ return form
#~ 
#~ def _parse_line_intensity(form, lill):
    #~ ### Line Intensity Lower Limits
    #~ if lill != None:
        #~ if lill[1].lower() == 'cdms_jpl':
            #~ form.find_control('lill_cdms_jpl').disabled = False
            #~ form['lill_cdms_jpl'] = str(lill[0])
        #~ elif lill[1].lower() == 'sijmu2':
            #~ form.find_control('lill_sijmu2').disabled = False
            #~ form['lill_sijmu2'] = str(lill[0])
        #~ elif lill[1].lower() == 'aij':
            #~ form.find_control('lill_aij').disabled = False
            #~ form['lill_aij'] = str(lill[0])
    #~ return form
#~ 
#~ def _parse_frequency_error_limit(form):
    #~ return form
#~ 
#~ def _set_settings(form):
    #~ # these settings are so that everything will be displayed in the 
    #~ # table then we get everything, and the user can choose AFTER if 
    #~ # they want it or not
    #~ #### Line Strength Display
    #~ form.find_control("ls1").get().selected = True
    #~ form.find_control("ls2").get().selected = True
    #~ form.find_control("ls3").get().selected = True
    #~ form.find_control("ls4").get().selected = True
    #~ form.find_control("ls5").get().selected = True
    #~ #### Energy Levels
    #~ form.find_control("el1").get().selected = True
    #~ form.find_control("el2").get().selected = True
    #~ form.find_control("el3").get().selected = True
    #~ form.find_control("el4").get().selected = True
    #~ #### Miscellaneous
    #~ form.find_control("show_unres_qn").get().selected = True
    #~ form.find_control("show_upper_degeneracy").get().selected = True
    #~ form.find_control("show_molecule_tag").get().selected = True
    #~ form.find_control("show_qn_code").get().selected = True
    #~ return form
#~ 
#~ def _get_results(form, dbg = False):
    #~ # click the form
    #~ clicked_form = form.click()
    #~ # then get the results page
    #~ result = mechanize.urlopen(clicked_form)
#~ 
    #~ #### EXPORTING RESULTS FILE
    #~ # so what I do is that I fetch the first results page,
    #~ # click the form/link to get all hits as a colon separated
    #~ # ascii table file
    #~ 
    #~ # get the form
    #~ resultform = mechanize.ParseResponse(result, backwards_compat=False)
    #~ result.close()
    #~ resultform = resultform[0]
    #~ # set colon as dilimeter of the table (could use anything I guess)
    #resultform.find_control('export_delimiter').items[1].selected =  True
    #~ resultform.find_control('export_delimiter').toggle('colon')
    #~ resultform_clicked = resultform.click()
    #~ result_table = mechanize.urlopen(resultform_clicked)
    #~ data = result_table.read()
    #~ result_table.close()
    #~ if dbg:
        #~ return resultform, result_table, data
    #~ else:
        #~ return data
#~ 
#~ def _parse_result(data, output='astropy.table'):
    #~ """
    #~ Only one output type at the moment    
    #~ """
    #~ if output == 'astropy.table':
        #~ # get each line (i.e. each molecule)
        #~ rows = data.split('\n')
        #~ # get the names of the columns
        #~ column_names = rows[0]
        #~ column_names = column_names.split(':')
        #~ 
        #~ for i in np.arange(len(column_names)):
            #~ column_names[i] = column_names[i].replace('<br>', ' ')
            #~ column_names[i] = column_names[i].replace('<sub>', '_')
            #~ column_names[i] = column_names[i].replace('<sup>', '^')
            #~ column_names[i] = column_names[i].replace('</sup>', '')
            #~ column_names[i] = column_names[i].replace('</sub>', '')
            #~ column_names[i] = column_names[i].replace('&#956;', 'mu')
            #~ column_names[i] = column_names[i].replace('sid[0] is null', '')
        #~ rows = rows[1:-1]
        #~ rows = [i.split(':') for i in rows]
        #~ rows = np.array(rows)
        #~ rows[rows == ''] = 'nan'
        #~ 
        #~ column_dtypes = ['str', 'str', 'float', 'float', 'float' , 'float' ,
                        #~ 'str', 'str', 'float',
                        #~ 'float', 'float', 'float', 'str', 'float', 'float',
                        #~ 'float', 'float', 'float', 'float','float','str']
        #~ column_units = [None, None, 'GHz?', 'GHz?', 'GHz?', 'GHz?', None, 
                        #~ None, '?', 'Debye^2', '?', 'log10(Aij)', '?', 
                        #~ 'cm^-1', 'K', 'cm^-1', 'K', None, None, None, None]
        #~ 
        #~ results = Table(data = rows , 
                        #~ names = column_names, 
                        #~ dtypes = column_dtypes)
        #~ 
        #~ for i in np.arange(len(column_units)):
            #~ results.field(i).units = column_units[i]
        #~ return results

