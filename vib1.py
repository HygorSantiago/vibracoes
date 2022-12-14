# https://www.youtube.com/watch?v=9mnNSMCu3dI

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy
from numpy import sqrt,sin,cos,exp

m = 1.
c = 1.
k = 100.
ti = 0.
tf = 10.
x0 = 1.
v0 = 0.
w = 5.
f = 10.
fi = 0.
ff = 2.
forca = 't'

def calculos(m,c,k,ti,tf,x0,v0,w,f):
	wn = (k/m)**0.5
	psi = c/(2*m*wn)
	wd = wn*(1-psi**2)**0.5
	cc = 2*m*wn
	t = np.linspace(ti,tf,1000)

	if c == 0.:
		theta = 3.1415/2
	if c != 0.:
		theta = np.arctan((wd*x0)/(v0+psi*wn*x0))
			
	if psi >= 1:
		A = 0
		x1 = 0
		x2 = 0
		xh = (x0+(v0+x0*wn)*t)*np.exp(-wn*t)
		wd = 0
	else:
		A = (((v0+psi*wn*x0)**2+(x0*wd)**2)/(wd)**2)**0.5
		x1 = A*np.sin(wd*t+theta)
		x2 = np.exp(-psi*wn*t)
		xh = x1*x2
		
	
	fig1,ax1 = plt.subplots()
	ax1.set_xlabel('Tempo [s]')
	ax1.set_ylabel('Deslocamento [m]')
	ax1.set_title('Resposta temporal')
	
	ax1.plot(t,xh,
             	 label='Resposta',
             	 color='black',
             	 linewidth=3)
             		
	if c != 0 and psi < 1:
		ax1.plot(t,x1,
				label='Resposta senoidal',
				color='blue',
				linewidth=1)
			
		ax1.plot(t,A*x2,
                		label='Resposta exponencial',
             			color='red',
             			linewidth=1)
		ax1.plot(t,-A*x2,
             			color='red',
             			linewidth=1)
             		
		ax1.legend()
		
	r = w/wn
	
	if r == 1 and psi == 0:
		Ay = (f*t)/(2*w)
		phi = t*0
		xpseno = np.sin(w*t - phi)
		xp = Ay*xpseno
		
	if abs(wn-w) < 0.05*w and psi == 0:
		phi = t*0
		xp = (f/2*w*(abs(w-wn)))*np.sin(w*t)*np.sin(abs(w-wn)*t)
		Ay = 0
	else:
		Ay = (f/(wn)**2)/(((1-r**2)**2+(2*psi*r)**2))**0.5
		phi = np.arctan((2*psi*r)/(1-r**2))
		xpseno = np.sin(w*t - phi)
		xp = Ay*xpseno
	
	x = xp+xh

	fig2,ax2 = plt.subplots()
	ax2.set_xlabel('Tempo [s]')
	ax2.set_ylabel('Deslocamento [m]')
	ax2.set_title('Resposta temporal')

	ax2.plot(t,xp,
             	label='Resposta parcial',
             	color='blue',
             	linewidth=1)
             	
	ax2.plot(t,xh,
             	label='Resposta homogĂȘnea',
             	color='red',
             	linewidth=1)
             	
	ax2.plot(t,x,
             	label='Resposta total',
             	color='black',
             	linewidth=3)
	
	ax2.legend()
	
	rpico = 1
	
	freq = np.linspace(fi,ff,1000)
	frf = (f/(wn)**2)/(((1-freq**2)**2+(2*psi*freq)**2))**0.5
	
	fig3,ax3 = plt.subplots()
	ax3.set_xlabel('r [ ]')
	ax3.set_ylabel('Fator de transmissibilidade [ ]')
	ax3.set_title('FunĂ§ĂŁo de resposta em frequĂȘncia')
	
	ax3.plot(freq,frf,
		 color='blue',
		 linewidth=2)
	
	fase = np.arctan((2*psi*freq)/(1-freq**2))
	
	fig4,ax4 = plt.subplots()
	ax4.plot(freq,fase)
	
	
	return wn,psi,wd,cc,A,theta,t,x1,x2,xh,fig1,r,Ay,phi,xp,x,fig2,rpico,freq,frf,fig3,fase,fig4
	
def laplace(forca,ti,tf,m,c,k):
	

	s = sympy.var('s')
	t = sympy.var('t')

	freq = np.linspace(ti,tf,1000)
	
	Fs = sympy.laplace_transform(forca, t, s, noconds=True) 
	ft = sympy.inverse_laplace_transform(Fs,s,t)
	ftd = [ft.subs({t:i}) for i in freq]
	ftd = np.array(ftd)

	Gs = (1/(m*(s**2)+c*s+k))
	Gs = sympy.nsimplify(Gs)
	gt = sympy.inverse_laplace_transform(Gs,s,t)
	gtd = [gt.subs({t:i}) for i in freq]
	gtd = np.array(gtd)
	
	ho = (1/(m*(s**2)+c*s+k))*Fs

	Hs = Gs*Fs
	Hs = Hs.apart(s)
	ht = sympy.inverse_laplace_transform(Hs,s,t)

	htd = []
	for i in freq:
		h2 = ht.subs({t:i})
		h2 = str(h2)
		h2 = eval(h2)
		htd.append(h2)
	
	fig,ax=plt.subplots()
	ax.plot(freq,htd,label='Resposta do sistema')
	ax.set_xlabel('Tempo [s]')
	ax.set_ylabel('Deslocamento [m]')
	ax.set_title('Resposta para forĂ§as de excitaĂ§ĂŁo')


	return Fs,ft,ftd,Gs,gt,gtd,Hs,ht,htd,fig,ho
	
def acao1(m,c,k,ti,tf,x0,v0,w,f):

	wn,psi,wd,cc,A,theta,t,x1,x2,xh,fig1,r,Ay,phi,xp,x,fig2,rpico,freq,frf,fig3,fase,fig4 = calculos(m,c,k,ti,tf,x0,v0,w,f)

	st.markdown('---')
		
	st.write(f'O sistema apresentado possui massa de {m} kg, amortecimento de {c} Ns/m e rigidez de {k} N/m. Estes sĂŁo chamados de parĂąmetros fĂ­sicos.')
		
	st.write(f'Os parĂąmetros modais sĂŁo calculados pelos fĂ­sicos e definem o sistema vibratĂłrio. A frequĂȘncia natural Ă© a frequĂȘncia com que o sistema oscila caso nĂŁo tenha nenhum tipo de amortecimento ou forĂ§a aplicada, neste caso tem o valor de {round(wn,3)} rad/s. O fator de amostecimento corresponde Ă  perda de energia ocasionada pelo amortecedor, Ă© de {round(psi,3)}, esta grandeza Ă© admensional. O Ășltimo parĂąmetro modal Ă© o modo, mas nĂŁo se aplica a 1 grau de liberdade.')
	
	st.latex(r'w_n = \sqrt{\frac{k}{m}}')
	st.latex(r'\zeta  = \frac{c}{2.m.w_n}')
	
	st.write(f'A frequĂȘncia com que o sistema nĂŁo forĂ§ado vibra Ă© a frequĂȘncia natural amortecida, {round(abs(wd),3)} rad/s. Ă inferior Ă  frequĂȘncia natural, caso o sistema seja sub-amortecido, pois Ă© influenciada pela perda de energia pelo amortecimento do sistema. No caso nĂŁo amortecido Ă© igual Ă  frequĂȘncia natural.')

	st.latex(r'w_d = \sqrt{1-\zeta ^2}')
	
	st.write(f'Com o aumento do amortecimento o sistema vai perdendo energia e o carĂĄter oscilatĂłrio. O ponto crĂ­tico Ă© quando o fator de amortecimento Ă© 1. A partir deste ponto o sistema nĂŁo mais vibra, apenas decai seu movimento exponencialmente atĂ© a estabilidade. Neste ponto o amortecimento Ă© chamado crĂ­tico e, neste exemplo Ă© de {round(cc,3)} Ns/m.')
	
	st.latex(r'c_c = 2.m.w_n')
	
	st.write('A soluĂ§ĂŁo da equaĂ§ĂŁo diferencial Ă© a soma da sua soluĂ§ĂŁo homogĂȘnea com sua soluĂ§ĂŁo parcial. A soluĂ§ĂŁo homogĂȘnea Ă© dada pela seguinte forma.')
	
	st.latex(r'\frac{d^2x(t)}{dt^2}.m + \frac{dx(t)}{dt}.c + x(t).k = 0')
	
	st.latex(r'x(t)=A.sen(s.t+\phi)')
	
	st.latex(r'\frac{dx(t))}{dt}=A.s.cos(s.t+\phi)')
	
	st.latex(r'\frac{dx^2(t))}{dt^2}=-A.s^2.sen(s.t+\phi)')
	
	st.write('Duas soluĂ§Ă”es sĂŁo admissĂ­veis, chamadas de raĂ­zes do polinĂŽmio caracterĂ­stico. Compoem um par complexo conjugado, jĂĄ nos parĂąmetros modais, na seguinte forma:')
	
	st.latex(r's_{1,2}=-\zeta . w_n \pm j.w_d')
	
	st.latex(f's_1={round(psi*wn,3)} - j.{round(wd,3)}')
	st.latex(f's_2={round(psi*wn,3)} + j.{round(wd,3)}')

def acao2(m,c,k,ti,tf,x0,v0,w,f):

	wn,psi,wd,cc,A,theta,t,x1,x2,xh,fig1,r,Ay,phi,xp,x,fig2,rpico,freq,frf,fig3,fase,fig4 = calculos(m,c,k,ti,tf,x0,v0,w,f)
	
	st.write('A soluĂ§ĂŁo homogĂȘnea tem a seguinte forma:')

	st.latex(r'x(t) = A . e^{ - \zeta . w_n . t} . sen(w_d . t + \theta)')
	
	st.write(f'A amplitude e fase do movimento Ă© encontrada segundo as condiĂ§Ă”es iniciais. Qualquer movimento vibratĂłrio nĂŁo forĂ§ado sĂł acontece com uma condiĂ§ĂŁo inicial de deslocamento, neste caso {x0} m e/ou velocidade, {v0} m/s. Substituindo na equaĂ§ĂŁo tĂȘm-se as seguintes conclusĂ”es:')
	
	st.latex(r'A = \sqrt{\frac{(v_0 + \zeta . w_n . x_0)^2 + (x_0 . w_d)^2}{w_d^2}}')
	st.latex(r'\theta = \frac{w_d . x_0}{v_0 + \zeta . w_n . x_0}')
	
	st.write(f'Amplitude e fase neste caso assumem os valores de {round(A,3)} m e {round(theta*180/3.1415)} graus.')

	st.write(f'Graficamente o movimento pode ser analisado como o seu deslocamento e funĂ§ĂŁo do tempo, entre {ti} s e {tf} s.')
		
	st.pyplot(fig1)
	
def acao3(m,c,k,ti,tf,x0,v0,w,f):

	wn,psi,wd,cc,A,theta,t,x1,x2,xh,fig1,r,Ay,phi,xp,x,fig2,rpico,freq,frf,fig3,fase,fig4 = calculos(m,c,k,ti,tf,x0,v0,w,f)
	
	st.write(f'A resposta parcial depende da frequĂȘncia da forĂ§a excitadora. O parĂąmetro r Ă© uma forma de adimensionalizar a frequĂȘncia. A amplitude da resposta pode ser dada em funĂ§ĂŁo de r, que nesse caso Ă© {round(r,3)}, assim como a fase:')
	
	st.latex(r'r=\frac{w}{w_n}')
	st.latex(r'X = \frac{\frac{f_0}{w_n^2}}{\sqrt{(1-r^2)^2+(2. \zeta r)^2}}')
	st.latex(r'\phi = \frac{2.\zeta . r}{1-r^2}')
	
	st.pyplot(fig2)
        
	st.write(f'Pela amplitude se calcula a transmissibilidade de movimento, isto Ă©, uma relaĂ§ĂŁo entre a amplitude da forĂ§a aplicada e a resposta. A mĂĄxima transmissibilidade ocorre quando a derivada temporal da amplitude da resposta parcial Ă© igual a zero.')

	st.latex(r'\frac{dX}{dr} = \frac{2.r(1-r^2-2.\zeta^2)}{[(1-r^2)^2+(2.\zeta .r)^2]^\frac{3}{2}} = 0')
	
	st.write('A anĂĄlise do dimĂ­nio da frequĂȘncia permite que se estude o comportamento do sistema diante a excitaĂ§ĂŁo de diferentes frequĂȘncias.')
	
	freq = np.linspace(fi,ff,1000)
	frf = (f/(wn)**2)/(((1-freq**2)**2+(2*psi*freq)**2))**0.5
	
	fig3,ax3 = plt.subplots()
	ax3.set_xlabel('r [ ]')
	ax3.set_ylabel('Fator de transmissibilidade [ ]')
	ax3.set_title('FunĂ§ĂŁo de resposta em frequĂȘncia, amplitude')
	
	ax3.plot(freq,frf,
		 color='blue',
		 linewidth=2)

	st.pyplot(fig3)
	
	fase = np.arctan((2*psi*freq)/(1-freq**2))
	
	fig4,ax4 = plt.subplots()
	ax4.set_xlabel('r [ ]')
	ax4.set_ylabel('Fase [graus]')
	ax4.set_title('FunĂ§ĂŁo de resposta em frequĂȘncia, fase')
	
	ax4.plot(freq,(180/3.1415)*fase,
		color='blue',
		 linewidth=2)
	
	st.pyplot(fig4)
	
def acao4(m,c,k,ti,tf,x0,v0,w,f,forca):
	
	wn,psi,wd,cc,A,theta,t,x1,x2,xh,fig1,r,Ay,phi,xp,x,fig2,rpico,freq,frf,fig3,fase,fig4 = calculos(m,c,k,ti,tf,x0,v0,w,f)
	
	Fs,ft,ftd,Gs,gt,gtd,Hs,ht,htd,fig,ho = laplace(forca,ti,tf,m,c,k)
	
	st.write('O sistema pode ser excitado por forĂ§as de diferentes formatos. Quando periĂłdicos as equaĂ§Ă”es diferenciais podem ser calculados, porĂ©m essa soluĂ§ĂŁo Ă© muito complexa para outros sistemas. Uma abordagem Ă© pela Transformada de Laplace onde o sistema Ă© formado por uma entrada (h(t)), uma saĂ­da (f(t)) e uma funĂ§ĂŁo de transferĂȘncia (g(t)) da seguinte forma:')
	
	st.latex(r'h(t)=g(t)\cdot f(t)')
	
	st.write('Onde g(t) Ă© a funĂ§ĂŁo de transferĂȘncia e f(t) a forĂ§a aplicada.')
	
	st.latex(r'g(t)=\frac{1}{\frac{d^2x(t)}{dt^2}.m + \frac{dx(t)}{dt}.c + x(t).k}')
	st.latex(f'f(t) = {forca}')
	
	st.write('Aplicando a Transformada de Laplace:')
	
	st.latex(f'H(s)=G(s) \cdot F(s)')
	
	st.write('Com F(s), G(s) e H(s) assumindo respectivamente os seguintes valores:')
	st.write(Fs)
	st.latex(r'G(s)=\frac{1}{m.s^2+c.s+k}')
	st.write(ho)
	
	st.write('Fazendo a transformada inversa de H(s) para h(t) temos:')
	st.write(ht)

	st.write('Graficamente a soluĂ§ĂŁo Ă©:')
	st.pyplot(fig)	
	
st.title('VibraĂ§ĂŁo Ă  excitaĂ§ĂŁo harmĂŽnica 1GDL')

st.write('Este trabalho aborda conceitos de vibraĂ§Ă”es de 1 GDL modelado segundo as seguintes equaĂ§Ă”es:')
st.latex(r'\frac{d^2x(t)}{dt^2}.m + \frac{dx(t)}{dt}.c + x(t).k = F_0.sen(w.t)')
st.latex(r'\frac{d^2x(t)}{dt^2} + \frac{dx(t)}{dt}.2.\zeta .w_n + x(t).w_n^2 = f_0.sen(w.t)')
st.write('Prof. Hygor Santiago, 2022')

with st.form('form1'):

	botao1 = st.form_submit_button(label='Calcular')
	
m = st.number_input(label='Insira a massa equivalente do sistema [Kg].',
				value=1.,
				min_value=0.00000000000001)
				
c = st.number_input(label='Insira o amortecimento equivalente do sistema [Ns/m].',
					value=1.,
					min_value=0.)
					
k = st.number_input(label='Insira a rigidez equivalente do sistema [N/m].',
				  value=100.,
				  min_value=0.)
				  
if botao1:
	acao1(m,c,k,ti,tf,x0,v0,w,f)
	
with st.form('form2'):
	botao2 = st.form_submit_button(label='Calcular')
				  
x0 = st.number_input(label='Insira o deslocamento inicial [m].',
					      value=1.)
					      
v0 = st.number_input(label='Insira a velocidade inicial [m/s].',
					    value=0.)
		    
ti = st.number_input(label='Insira o tempo inicial de exibiĂ§ĂŁo [s].',
				       value=0.,
				       min_value=0.)
				       
tf = st.number_input(label='Insira o tempo final de exibiĂ§ĂŁo [s].',
				     value=ti+10.,
				     min_value=ti)
				     
if botao2:
	acao2(m,c,k,ti,tf,x0,v0,w,f)
					     
				    
with st.form('form3'):
	botao3 = st.form_submit_button(label='Calcular')
	
f = st.number_input(label='Insira a amplitude da forĂ§a aplicada [N].',
				     value=10.)
				     
w = st.number_input(label='Insira a frequĂȘncia da forĂ§a aplicada [rad/s].',
				     value=5.)
				     
fi = st.number_input(label='Insira a frequĂȘncia inicial de exibiĂ§ĂŁo [rad/s].',
				       value=0.,
				       min_value=0.)
				       
ff = st.number_input(label='Insira a frequĂȘncia final de exibiĂ§ĂŁo [rad/s].',
				     value=ti+2.,
				     min_value=ti)
	
if botao3:
	acao3(m,c,k,ti,tf,x0,v0,w,f)


with st.form('form4'):
	botao4 = st.form_submit_button(label='Calcular')
	
forca = st.text_input(label='Insira a forĂ§a aplicada em funĂ§ĂŁo de t.',
				     value='t')
				     
if botao4:
	acao4(m,c,k,ti,tf,x0,v0,w,f,forca)
