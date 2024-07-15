********************************************************************************
* QLAB - CURSO BIG DATA & ANALYTICS PARA LA GESTIÓN PÚBLICA PERUANA
*
* Autores	 : 	Diego Delgado 
*			 	Alvaro Zapata
*				Maria Venero
*				Julissa Menchola
*
* Description: 	Trabajo grupal 1 - Teoria de muestreo
* 
* 				 Julio 2024
*
********************************************************************************
* ******************************************************************************
* Paths
*


**# Paso 1: Cargar data
 
	gl data "C:\Users\DDelgado\Documents\Diplomado QLAB\Big Data and Analytics\TG1"
	
	
	import spss "$data/01_PENALES_CARATULA.sav" , clear
	
	des, short
	
	des
	
	ren *, lower
**# Paso 2

	gen pp_dcsp = delito_generico == "DELITOS CONTRA LA SEGURIDAD PUBLICA"
	tab pp_dcsp, m

**# Paso 3

	set seed 20171341


**# Paso 4
	egen strata = group(ccdd genero pp_dcsp) // 91 estratos como resultado
	
	gen fpc_pp = .
	gen pweight = .
	

	forvalues i = 1/91 {
		
		count if strata == `i'
		
		local N_strata 	= `r(N)'
		local n_strata 	= round(0.04*`N_strata')
		local pweight 	=  `N_strata'/`n_strata'
		
		replace	fpc_pp 	= `N_strata'  if strata == `i'
		replace	pweight =  `pweight' if strata == `i'
		
	}
	
	sample 4 , by(strata)
	
		
	count // 3,038 obs

**# Paso 5
	
	svyset [pweight = pweight] , strata(strata) 	fpc(fpc_pp)		

	svy: tab pp_dcsp , // 25.27% de la poblacion habrian cometido delitos "Delitos contra la seguridad pública"
	svy: tab pp_dcsp , ci count format(%9.0f) // 19,206 personas habrian cometido delitos "Delitos contra la seguridad pública"
	
