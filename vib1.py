# https://www.youtube.com/watch?v=9mnNSMCu3dI

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def ParametrosModais(m,c,k,ti,tf,x0,v0):
	
	if m == 0:
		wn = 'A massa deve ser diferente de zero.'
		psi = 'A massa deve ser diferente de zero.'
	else:
		wn = (k/m)**0.5
		psi = c/(2*m*wn)
	
		wd = wn*(1-psi**2+0.000000001)**0.5
		cc = 2*m*wn
    		
		A = (((v0+psi*wn*x0)**2+(x0*wd)**2)/(wd)**2)**0.5
		theta = np.arctan((wd*x0)/(v0+psi*wn*x0+0.000000001))

		t = np.linspace(ti,tf,1000)
		x1 = A*np.sin(wd*t+theta)
		x2 = np.exp(-psi*wn*t)
		x = x1*x2
    
		fig,ax = plt.subplots()
		ax.set_xlabel('Tempo [s]')
		ax.set_ylabel('Deslocamento [m]')
		ax.set_title('Resposta temporal')
	
	
		ax.plot(t,x,
             		label='Resposta',
             		color='black',
             		linewidth=3)
             		
		if c != 0 and psi < 1:
			ax.plot(t,x1,
				label='Resposta senoidal',
				color='blue',
				linewidth=1)
			
			ax.plot(t,A*x2,
                		label='Resposta exponencial',
             			color='red',
             			linewidth=1)
			ax.plot(t,-A*x2,
             			color='red',
             			linewidth=1)
             		
			ax.legend()
			
             			
	return wn,psi,wd,cc,fig,A,theta
	
st.title('Vibração livre 1GDL')

entrada_massa = st.number_input(label='Insira a massa equivalente do sistema [Kg].',
				value=1.)
entrada_amortecimento = st.number_input(label='Insira o amortecimento equivalente do sistema [Ns/m].',
					value=0.)
entrada_rigidez = st.number_input(label='Insira a rigidez equivalente do sistema [N/m].',
				  value=100.)
	
entrada_descolamentoinicial = st.number_input(label='Insira o deslocamento inicial [m].',
					      value=1.)
					      
entrada_velocidadeinicial = st.number_input(label='Insira a velocidade inicial [m/s].',
					    value=0.)
					    
entrada_tempoinicial = st.number_input(label='Insira o tempo inicial de exibição [s].',
				       value=0.)
				       
entrada_tempofinal = st.number_input(label='Insira o tempo final de exibição [s].',
				     value=10.)
		
with st.form('teste'):
	botao_calcular = st.form_submit_button(label='Calcular')
				
if botao_calcular:
	
	wn,psi,wd,cc,fig,A,theta = ParametrosModais(entrada_massa,
				  entrada_amortecimento,
				  entrada_rigidez,
				  entrada_tempoinicial,
				  entrada_tempofinal,
				  entrada_descolamentoinicial,
				  entrada_velocidadeinicial)
	
	st.markdown('---')
				  
	st.write('Parêmetros físicos:')
	st.write(f'Massa: {entrada_massa} Kg')
	st.write(f'Amortecimento: {entrada_amortecimento} Ns/m')
	st.write(f'Rigidez: {entrada_rigidez} N/m')
	
	st.markdown('---')
	
	st.write('Parêmetros modais:')
	
	st.latex(r'w_n = \sqrt{\frac{k}{m}}')
	st.latex(r'\zeta  = \frac{c}{2.m.w_n}')
	
	st.write(f'Frequência natural: {round(wn,3)} rad/s')
	st.write(f'Fator de amortecimento: {round(psi,4)}')
	
	st.markdown('---')
	
	st.write('Outros parâmetros:')
	
	st.latex(r'w_d = \sqrt{1-\zeta ^2}')
	st.latex(r'c_c = 2.m.w_n')
	
	st.write(f'Frequência natural amortecida: {round(wd,3)} rad/s')
	st.write(f'Amortecimento crítico: {round(cc,3)} Ns/m')
	
	st.markdown('---')
	
	st.write('Raízes do polinômio característico:')
	
	st.latex(r's_{1,2} = - \zeta . w_n \pm j . w_d')
	
	st.write(f's = - {round(psi*wn,2)} - j{round(wd,2)}')
	st.write(f's = - {round(psi*wn,2)} + j{round(wd,2)}')
	
	st.markdown('---')
	
	st.write('Resposta temporal')
	st.latex(r'x(t) = A . e^{ - \zeta . w_n . t} . sen(w_d . t + \theta)')
	st.latex(r'A = \sqrt{\frac{(v_0 + \zeta . w_n . x_0)^2 + (x_0 . w_d)^2}{w_d^2}}')
	st.latex(r'\theta = \frac{w_d . x_0}{v_0 + \zeta . w_n . x_0}')
	
	st.write(f'Amplitude: {round(A,3)} m')
	st.write(f'Fase: {round(theta*180/3.1415,3)} graus')
	
	st.markdown('---')

	st.pyplot(fig)

