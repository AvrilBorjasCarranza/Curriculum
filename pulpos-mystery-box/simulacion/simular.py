#!/usr/bin/env python3
"""Simulación de 100 clientes inventados para OctoMood. NO son datos reales: son supuestos para detectar puntos débiles.
Cada cliente: (segmento, nº, disposición a pagar media €, desviación, interés por la caja misterio/kawaii 0-1, confianza en vendedor nuevo 0-1)."""
import math, random, json
random.seed(7)
SEG = [
 ("Fans de blind boxes / kawaii (18-30)", 18, 18, 6, .80, .55),
 ("Adolescentes (13-17), poca paga",       12,  8, 3, .70, .50),
 ("Estudiantes con presupuesto justo",     14, 10, 4, .55, .55),
 ("Amigos y familia (apoyo)",               8, 15, 5, .65, .95),
 ("Aficionados a la impresión 3D",         10,  6, 3, .40, .55),
 ("Compradores de regalo (padres, colegas)",12, 12, 4, .50, .60),
 ("Curiosos sin intención de compra",      16,  6, 3, .35, .45),
 ("Revendedores / coleccionistas",          4, 14, 4, .50, .50),
 ("Comunidad local de Metz (mercadillos)",  6, 15, 5, .55, .70),
]
def phi(x): return 0.5*(1+math.erf(x/math.sqrt(2)))
def prob(seg, price, ship):
    _, n, mu, sd, interest, trust = seg
    return interest * trust * (1 - phi((price+ship-mu)/sd))
def run(price, ship):
    rows=[(s[0], s[1], s[1]*prob(s, price, ship)) for s in SEG]
    return rows, sum(r[2] for r in rows)
out={}
for label, price, ship in [("14,99 € + envío 4,50 €",14.99,4.5),("14,99 € en mano (Metz)",14.99,0),("12,99 € + envío 4,50 €",12.99,4.5),("9,99 € + envío 4,50 €",9.99,4.5),("17,99 € + envío 4,50 €",17.99,4.5)]:
    rows,t=run(price,ship); out[label]={"compradores_de_100":round(t,1),"por_segmento":{r[0]:round(r[2],1) for r in rows}}
    print(f"{label:28s} → {t:5.1f} compradores de 100")
print()
rows,_=run(14.99,4.5)
for r in sorted(rows,key=lambda x:-x[2]): print(f"{r[0]:42s} {r[1]:2d} personas → {r[2]:.1f} compran")
# ingresos y margen aproximados a 14,99 € con envío: 5,85 € de coste completo por pieza
for label,p,s in [("14,99 € + envío",14.99,4.5),("12,99 € + envío",12.99,4.5),("9,99 € + envío",9.99,4.5)]:
    _,t=run(p,s); print(f"{label}: ingreso por 100 expuestos = {t*p:.0f} €, margen sobre coste 5,85 € = {t*(p-5.85):.0f} €")
json.dump(out,open("resultado.json","w"),indent=1,ensure_ascii=False)
