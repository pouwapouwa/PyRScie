# -*- coding: utf-8 -*-

classe_url_licence = [
    ["IN400A1", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g74276", "L2 Info."],
    ["IN400A2", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g74298", "L2 Info."],
    ["IN400A3", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g109220", "L2 Info."],
    ["IN400A4", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g154461", "L2 Info."],
    ["IN400A", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g72962", "L3 Info."],
    ["IN601A1", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g72873", "L3 Info."],
    ["IN601A2", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g72874", "L3 Info."],
    ["IN601A3", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g72875", "L3 Info."],
    ["IN601A", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g72871", "L3 Info."],
    ["IN602", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g57803", "L3 Info. Gestion"],
    ["MI201A1", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80988", "L1"],
    ["MI201A2", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80989", "L1"],
    ["MI201A3", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80990", "L1"],
    ["MI201A4", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80991", "L1"],
    ["MI201A5", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80992", "L1"],
    ["MI201A6", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80993", "L1"],
    ["MI201A7", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g199195", "L1"],
    ["MI201A8", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g237450", "L1"],
    ["MI201A9", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g241663", "L1"],
    ["MI201", "https://edt-st.u-bordeaux.fr/etudiants/Licence/Semestre2/g80987", "L1"]
]

classe_url_master = [
    ["IN811", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g56003", "Info. AMF"],
    ["IN820", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g55808", "Info/Math Crypto et Sécu. Info."],
    ["IN830", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g56017", "Info. Génie Log."],
    ["IN840", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g56028", "Info. Image, Son, Vidéo"],
    ["IN850", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g56036", "Info. Réseaux, Systèmes et Mobilité"],
    ["MA820", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master1/Semestre2/g112167", "Maths. Crypto et Sécu. Info."]
]

classe_url_master2 = [
    ["IN011", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56008", "Info. AMF"],
    ["IN031", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56021", "Info. Génie Log. Conduite de Projet"],
    ["IN032", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56023", "Info. Génie Log. Archi Log."],
    ["IN041", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56031", "Info. ISV 3D"],
    ["IN042", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56033", "Info. ISV Son/Vidéo"],
    ["IN051", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56039", "Info. RSM Calcul Haute Performance"],
    ["IN052", "https://edt-st.u-bordeaux.fr/etudiants/Master/Master2/Semestre2/g56042", "Info. RSM"]
]

classe_url = classe_url_licence + classe_url_master + classe_url_master2


def find_user_and_group(u_t_g, nick):
    t = []
    for i in range(len(u_t_g)):
        if u_t_g[i][0] == nick:
            for j in range(1,len(u_t_g[i])):
                t = t + [u_t_g[i][j]]
    return t


def RepresentsInt(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def add_user_and_group(u_t_g, nick, grp):
    for i in range(len(u_t_g)):
        if u_t_g[i][0] == nick:
            for j in range(1,len(u_t_g[i])):
                if u_t_g[i][j] == grp:
                    return u_t_g
            u_t_g[i] = u_t_g[i] + [grp]
            return u_t_g
    u_t_g = u_t_g + [[nick, grp]]
    return u_t_g
            

def del_user_and_group(u_t_g, nick, grp):
    for i in range(len(u_t_g)):
        if u_t_g[i][0] == nick:
            T = []
            if (len(u_t_g[i]) == 2 and u_t_g[i][1] == grp):
                del u_t_g[i]
                return u_t_g
            else:
                for j in range(len(u_t_g[i])):
                    if u_t_g[i][j] != grp:
                        T = T + [u_t_g[i][j]]
                u_t_g[i] = T
                return u_t_g
    return u_t_g

def rewrite_user_to_group(u_t_g):
    file = open('user_to_group.py', 'w')
    file.write("# -*- coding: utf-8 -*-")
    file.write("\nu_t_g = [")

    for i in range(len(u_t_g)-1):
        file.write("[")
        for j in range(len(u_t_g[i])-1):
            file.write("\"" + u_t_g[i][j] + "\", ")
        file.write("\"" + u_t_g[i][len(u_t_g[i])-1] + "\"], ")


    file.write("[")
    for j in range(len(u_t_g[len(u_t_g)-1])):
        file.write("\"" + u_t_g[len(u_t_g)-1][j] + "\", ")
    file.write("\"" + u_t_g[len(u_t_g)-1][len(u_t_g[len(u_t_g)-1])-1] + "\"]")

    file.write("]")
    file.close()

def di(args):
    if "di" in args:
        l = 0
        size = len(args)
        T = ""
        bool = False
        while (l < size-1 and not (args[l] == "d" and args[l+1] == "i")):
            l += 1 
        if (l+2 < size and (args[l+2] == "s" or args[l+2] == "t")):
            if (l+3 < size and (args[l+3] == " " or args[l+3] == "-")):
                u = l+3+1
                while (u < size and args[u] != " "):
                    T += str(args[u])
                    u += 1
                return T
            u = l + 2
            while (u < size and args[u] != " "):
                T += str(args[u])
                u += 1
            return T
        u = l + 2
        while (u < size and args[u] != " "):
            T += str(args[u])
            u += 1
        return T
    return ""
                
        
def rewrite_jokes(joke):
    file = open('jokes.py', 'w')
    file.write("# -*- coding: utf-8 -*-")
    file.write("\njokes = [")
    
    for i in range(len(joke)-1):
        file.write("[\"" + joke[i][0] + "\"], ")
    file.write("[\"" + joke[len(joke)-1][0] + "\"]")

    file.write("]")
    file.close()
