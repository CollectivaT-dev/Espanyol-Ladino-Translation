import main
import util
import pytest

ROOT_DIC = "resource/lista_verbos_ladino_conjugados.txt"
ROOT_DIC_N = "resource/lista_palabras_ladino.txt"
ROOT_DIC_P = "resource/dic_esp_lad_phr_v2.txt"

print("Reading dictionary of verbs", ROOT_DIC)

dic_verb = util.get_dic(ROOT_DIC)
print("%i entries"%len(dic_verb))


print("Reading dictionary of nouns", ROOT_DIC_N)

dic_noun = util.get_dic(ROOT_DIC_N)
print("%i entries"%len(dic_noun))

print("Reading dictionary of phrases", ROOT_DIC_P)
    
dic_phrase = util.get_dic(ROOT_DIC_P)
print("%i entries"%len(dic_phrase))

trans = lambda x: main.translate(x, dic_verb, dic_noun, dic_phrase)


vosotros_tests = [("estáis", "estash"),
				  ("miráis", "mirash"),
				  ("tenéis", "tenesh"),
				  ("hacéis", "azesh"),
				  ("queréis", "keresh"),
				  ("sabéis", "savesh"),
				  ("veis", "vesh"),
				  ("oís", "oyish"),
				  ("vivís", "bivish"),
				  ("venís", "vinish"),
				  ("decís", "dizish"),
				  ("salís", "salish"),
				  ("tendríais", "tendriash")]

@pytest.mark.parametrize(('x', 'y'), vosotros_tests)
def test_vosotros(x, y):
    pytest.assume(trans(x) == y)


perfect_conversions = [('he venido', 'vini'),
					   ('he dicho', 'dizi'),
					   ('he hecho', 'ize'),
					   ('has hecho', 'izites'), #si escribes "tu has hecho" si sale"
					   ('ha hecho', 'izo'),
					   ('hemos hecho', 'izimos'),
					   ('habéis hecho', 'izitesh'),
					   ('han hecho', 'izyeron'),
					   ('habéis comido', 'komitesh'),
					   ('hemos abrazado', 'abrasimos'),
					   ('habéis abrazado','abrasatesh'),
					   ('has bebido', 'bevites'),
					   ('hemos bebido', 'bevimos'),
					   ('han abierto', 'avrieron'),
					   ('hemos abierto', 'avrimos'),
					   ('he querido', 'kije'),
					   ('hemos querido', 'kijimos'),
					   ('habéis querido', 'kijitesh'),
					   ('he sabido', 'supe'),
					   ('has sabido', 'supites'),
					   ('ha sabido', 'supo'),
					   ('hemos sabido', 'supimos'),
					   ('habéis sabido', 'supitesh'),
					   ('han sabido', 'supyeron')]

@pytest.mark.parametrize(('x', 'y'), perfect_conversions)
def test_perfect(x, y):
    pytest.assume(trans(x) == y)


imperative_vosotros = [("no salgáis", "no salgash"),
						("no vengáis", "no vengash"),
						("no digais", "no digash"),
						("no vayais", "no vaygash"),
						("no conozcas", "no konoskash"),
						("no traigas", "no traigash")]

@pytest.mark.parametrize(('x', 'y'), imperative_vosotros)
def test_imperative_vosotros(x, y):
    pytest.assume(trans(x) == y)

haber = [('hay', 'ay'), ('había', 'avia'), ('hubo', 'uvo'), ('habrá', 'avra'),
   		 ('habría', 'avria'), ('haya', 'ayga'), ('hubiera', 'uvyera')]

@pytest.mark.parametrize(('x', 'y'), haber)
def test_haber(x, y):
    pytest.assume(trans(x) == y)

#TODO: extend this...
conjugations = [('supongo', 'supozo'),
				('propongo', 'propozo'),
				('perder', 'pedrer'),
				('pierde', 'pedra'),
				('vivo', 'bivo'),
				('estas cocinando', 'estas gizando'),
				('estás cocinando', 'estas gizando'),
				('estoy llamando', 'esto yamando'),
				('agradezco', 'agradesko'),
				('habras terminado', 'avras eskapado')]

@pytest.mark.parametrize(('x', 'y'), conjugations)
def test_perfect(x, y):
    pytest.assume(trans(x) == y)

future_conversion = [('telefonaré', 'va telefonar'),
					 ('telefonarás', 'vas a telefonar'),
					 ('telefonará', 'va telefonar'),
					 ('telefonaremos', 'vamos a telefonar'),
					 ('telefonaréis', 'vash a telefonar'),
					 ('telefonarán', 'van a telefonar'),
					 ('pondré', 'va meter'),
					 ('abriremos', 'vamos a avrir'),
					 ('abriréis', 'vash a avrir'),
					 ('querremos', 'vamos a kerer'),
					 ('querrá', 'va a kerer'),
					 ('sabrán', 'van a saver'),
					 ('dirán', 'van a dizir')]

@pytest.mark.parametrize(('x', 'y'), future_conversion)
def test_future_conversion(x, y):
    pytest.assume(trans(x) == y)

tener_que = [("tengo que", "devo de"),
			("tienes que", "deves de"),
			("tiene que", "deve de"),
			("tenemos que", "devemos de"),
			("teneis que", "devesh de"),
			("tienen que", "deven de")]

@pytest.mark.parametrize(('x', 'y'), tener_que)
def test_tener_que(x, y):
    pytest.assume(trans(x) == y)

hay_que = [('hay que', 'kale')]

@pytest.mark.parametrize(('x', 'y'), hay_que)
def test_hay_que(x, y):
    pytest.assume(trans(x) == y)

sentences = [("Ellos quieren casarse", "Eyos keren kazarse"),
			 ("Cuando Sara prepara la mesa, siempre pone flores y mantel de encaje",
			  "Kuando Sara apareja la meza, siempre mete rozas i mantel de dantela"),
			 ("Sara lee libros de aventura.","Sara melda livros de aventura."),
			 ("En otoño empiezan las lluvias. Esto es bueno porque las presas se llenan de agua.",
			  "En otonyo empesan las luvyas. Esto es bueno porke las presas se inchan de agua."),
			 ("Venid aquí", "Veni aki"),
			 ('esta leyendo', 'esta meldando'),
			 ('esto es una cocina', 'esto es una mupak'),
			 ('hay que dejar', 'kale deshar'),
			 ("suele ser", "debe ser"),
			 ("solian", "debian ser"),
			 ("soy profesora", "so profesora"),
			 ("Es decir, yo voy.", "Es dizir, yo vo."),
			 ("No utilizo mucho mi ordenador.", "No kullaneo muncho mi ordenador."),
			 ("Ella es marroquí", "Eya es marokino/a")]

@pytest.mark.parametrize(('x', 'y'), sentences)
def test_sentences(x, y):
    pytest.assume(trans(x) == y)


#NOTE: if this is too hard to implement, better make the translations as in famozo/a
gender = [('famosa', 'famoza'),
		 ('famoso', 'famozo'),
		 ('rubia', 'blonda'),
		 ('rubio', 'blondo'),
		 ('cansada', 'kansada'),
		 ('cansado', 'kansado'),
		 ('blanca','blanka'),
		 ('blanco', 'blanko')]

@pytest.mark.parametrize(('x', 'y'), gender)
def test_gender(x, y):
    pytest.assume(trans(x) == y)



other = [('te', 'te'),
		 ('té', 'chay'),
		 ("Moshe y Avram", "Moshe i Avram"),
		 ("Mexicano", "Meksikano"),
		 ("experto", "eksperto"),
		 ("gobernador", "governador"),
		 ("añadir", "anyadir"),
		 ("vosotros", "vozotros"),
		 ("timbre", "sonido"),
		 ("proponer", "propozar"),
		 ('suponer', 'supozar'),
		 ('poner', 'meter'),
		 ('pongo', 'meto'),
		 ('pones', 'metes'),
		 ('decir', 'dizir'),
		 ('asesinar', 'asasinar'),
		 ('abuela', 'gramama'),
		 ('abuelo', 'granpapa'),
		 ('bisabuelo', 'bizgranpapa'),
		 ('bisabuela', 'bizgramama'),
		 ('sobrino', 'sovrino'),
		 ('sobrina', 'sovrina'),
		 ('maravillosa', 'maraviyoza'),
		 ('gente', 'djente'),
		 ('champú', 'shampuan'),
		 ('ordenador', 'ordenador'),
		 ('creendo', 'kreyendo'),
		 ('comía', 'komia'),
		 ('obligado', 'ovligado'),
		 ('bailar', 'baylar'),
		 ('bailamos', 'baylamos'),
		 ('pueden', 'pueden'),
		 ('existir', 'egzistir'),
		 ('cual', 'kual'),
		 ('palabra', 'biervo'),
		 ('bañarse', 'benyarse'),
		 ('estás yendo', 'estas indo')]

@pytest.mark.parametrize(('x', 'y'), other)
def test_other(x, y):
    pytest.assume(trans(x) == y)
    
    
new = [('operación', 'operasion'),
		 ('hola', 'ola'),
		 ("aguadito", "agadito"),
		 ("queso", "kezo"),
		 ("experto", "eksperto"),
		 ("gobernador", "governador"),
		 ("llamachay", "yamachay"),
		 ("ñandu", "nyandu"),
		 ("scraft", "skraft")]

@pytest.mark.parametrize(('x', 'y'), new)
def test_new(x, y):
    pytest.assume(trans(x) == y)
