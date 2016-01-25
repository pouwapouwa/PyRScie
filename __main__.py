#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Example program using ircbot.py.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
ircbot.py.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

import time
import re

from parse_file import *
from edt import *
from jokes import *
from user_to_group import *
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

command = ['!stats', '!edt', '!joke']
edt_opt = [['numéro_groupe', "\'!edt i\' pour obtenir l'url du ième groupe que tu as enregistré. Si aucun groupe n'est précisé, le 1er de la liste est choisi automatiquement."], 
           ['identifiant_groupe', "\'!edt XXXX\' pour obtenir l'url du groupe XXXX."], 
           ['groups', "\'!edt groups\' pour afficher l'ensemble des groupes enregistrés."], 
           ['add', "\'!edt add XXXX\' pour ajouter le groupe XXXX à votre sélection."],
           ['delete', "\'!edt delete XXXX\' pour supprimer le groupe XXXX de votre sélection."],
           ['today', "\'!edt today\' pour obtenir la liste des cours de la journée, à combiner avec un numéro ou identifiant de groupe (le groupe par défaut est le 1er enregistré)."], 
           ['tomorrow', "\'!edt tomorrow\' pour obtenir la liste des cours de demain, à combiner avec un numéro ou identifiant de groupe (le groupe par défaut est le 1er enregistré)."], 
           ['now', "\'!edt now\' pour obtenir la liste des prochains cours d'aujourd'hui, à combiner avec un numéro ou identifiant de groupe (le groupe par défaut est le 1er enregistré)."], 
           ['licence', "\'!edt licence\' donne la liste des groupes disponibles en Licence."], 
           ['master', "\'!edt master\' donne la liste des groupes disponibles en Master."], 
           ['master2', "\'!edt master2\' donne la liste des groupes disponibles en Master2."], 
           ['help', "\'!edt help\' suivie d'une commande donne des  informations sur celle-ci.  Sinon, vous aide juste à comprendre le fonctionnement de \'!edt\'."]]
bool = False


def get_args(a):
    text = '' #String
    for i in range(len(a)):
        text = text + a[i]
    return text

class TestBot(SingleServerIRCBot):

    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.user_to_group = u_t_g
        self.jokes = jokes
        self.bool = False

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        #c.privmsg(self.channel, "Bonjour tout le monde :D")

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments()[0])

    #def on_pubmsg(self, c, e):
    #    a = e.arguments()
    #    text = get_args(a)
    #    nick = nm_to_n(e.source())

    #    if (("oui" in str(text).lower()) and (self.bool == True)):
    #        c.privmsg(self.channel, "Hum, j'aime pas trop beaucoup ça ...")

    #    elif (("non" in str(text).lower()) and (self.bool == True)):
    #        c.privmsg(self.channel, "Ouf. J'avais les oreilles qui sifflent ...")

    #    self.bool = False

    #    tmp = di(text)
    #    if len(tmp) != 0:
    #        c.privmsg(self.channel, tmp)

    #    if c.get_nickname() in text:
    #        c.privmsg(self.channel, "On parle de moi ?")
    #        self.bool = True

    #    if (str(text) == str(text).upper() and str(text).isalnum() and not str(txt).isdigit()):
    #        c.privmsg(self.channel, "ON NE CRIE PAS ICI, SVP !")

    #    if "bonjour" in str(text).lower():
    #        c.privmsg(self.channel, "Bonjour " + nick + " !")

    #    if "bonsoir" in str(text).lower():
    #        c.privmsg(self.channel, "Bonsoir " + nick + " !")

    #    if "\o/" in text:
    #        c.action(self.channel, "siffle avec ses dents !")

    #def on_dccmsg(self, c, e):
    #    c.privmsg("Tu viens de dire : " + e.arguments()[0])

    #def on_dccchat(self, c, e):
    #    if len(e.arguments()) != 2:
    #        return
    #    args = e.arguments()[1].split()
    #    if len(args) == 4:
    #        try:
    #            address = ip_numstr_to_quad(args[2])
    #            port = int(args[3])
    #        except ValueError:
    #            return
    #        self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection
        try:
            count = len(re.findall(r'\w+', cmd))
            arguments = (e.arguments())[0].split()
            find = find_user_and_group(self.user_to_group, nick)
            text = ""
        
            if arguments[0][0] == "\'":
                c.privmsg(nick, "Essaie sans l'apostrophe ;)")

            elif (cmd == "!disconnect") and (nick == "Pouwapouwa"):
                self.disconnect()

            elif (cmd == "!die") and (nick == "Pouwapouwa"):
                self.die()

            elif cmd == "!stats":
                for chname, chobj in self.channels.items():
                    c.privmsg(nick, "--- Channel statistques ---")
                    c.privmsg(nick, "Channel: " + chname)
                    users = chobj.users()
                    users.sort()
                    c.privmsg(nick, "Users: " + ", ".join(users))
                    opers = chobj.opers()
                    opers.sort()
                    c.privmsg(nick, "Opers: " + ", ".join(opers))
                    voiced = chobj.voiced()
                    voiced.sort()
                    c.privmsg(nick, "Voiced: " + ", ".join(voiced))

            elif (cmd == "!dcc") and (nick == "Pouwapouwa"):
                dcc = self.dcc_listen()
                c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                    ip_quad_to_numstr(dcc.localaddress),
                    dcc.localport))       

####### EDT

            elif "!edt" in cmd:
                       
                if ((len(arguments) == 1) and (len(find) == 0)):
                    c.privmsg(nick, "Il faut enregistrer un groupe ou alors rajouter des arguments. Pourquoi ne pas tenter \'!edt help\' ?")

                elif (len(arguments) == 1):
                    edt = find[0]
                    for i in range(len(classe_url)):
                        if classe_url[i][0] == edt:
                            text =  classe_url[i][0] + ": " + classe_url[i][1] + ".html "
                            c.privmsg(nick, text)
                            return
                    c.privmsg(nick, "Je n'ai pu trouver le groupe " + edt + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")

                elif arguments[1] == "licence":
                    if len(arguments) == 2:
                        text = "Groupes de Licence proposés : "
                        for i in range(len(classe_url_licence)-1):
                            text = text + classe_url_licence[i][0] + " - " + classe_url_licence[i][2] + ", "
                        text = text + classe_url_licence[len(classe_url_licence)-1][0] + " - " + classe_url_licence[len(classe_url_licence)-1][2]
                        c.privmsg(nick, text)
                        text = "Utilise \'!edt\' suivi de l'identifiant de l'emploi du temps pour obtenir l'url de l'emploi du temps concerné. Ex: \'!edt MI201\'."
                        c.privmsg(nick, text)
                        
                elif arguments[1] == "master":
                    if len(arguments) == 2:
                        text = "Groupes de Master proposés : "
                        for i in range(len(classe_url_master)-1):
                            text = text + classe_url_master[i][0] + " - " + classe_url_master[i][2] + ", "
                        text = text + classe_url_master[len(classe_url_master)-1][0] + " - " + classe_url_master[len(classe_url_master)-1][2]
                        c.privmsg(nick, text)
                        text = "Utilise \'!edt\' suivi de l'identifiant de l'emploi du temps pour obtenir l'url de l'emploi du temps concerné. Ex: \'!edt IN811\'."
                        c.privmsg(nick, text)

                elif arguments[1] == "master2":
                    if len(arguments) == 2:
                        text = "Groupes de Master2 proposés : "
                        for i in range(len(classe_url_master2)-1):
                            text = text + classe_url_master2[i][0] + " - " + classe_url_master2[i][2] + ", "
                        text = text + classe_url_master2[len(classe_url_master2)-1][0] + " - " + classe_url_master2[len(classe_url_master2)-1][2]
                        c.privmsg(nick, text)
                        text = "Utilise \'!edt\' suivi de l'identifiant de l'emploi du temps pour obtenir l'url de l'emploi du temps concerné. Ex: \'!edt IN011\'."
                        c.privmsg(nick, text)

                elif RepresentsInt(arguments[1]):
                    if ((arguments[1] >= len(find)) or (arguments[1] <= 0)):
                        c.privmsg(nick, "Et faut pas me prendre pour une idiote ! Tu demandes un numéro de groupe que tu n'as pas ;)")
                        return
                    edt = find[int(arguments[1])-1]
                    for i in range(len(classe_url)):
                        if classe_url[i][0] == edt:
                            text =  classe_url[i][0] + ": " + classe_url[i][1] + ".html "
                            c.privmsg(nick, text)
                            return
                    c.privmsg(nick, "Je n'ai pu trouver le groupe " + edt + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")

                elif ((arguments[1] == "today") or (arguments[1] == "tomorrow")):
                    if arguments[1] == "today":
                        d = 0
                        t = "aujourd'hui"
                    else:
                        d = 1
                        t = "demain"
                    find = find_user_and_group(self.user_to_group, nick)

                    if (len(arguments) == 2):
                        if len(find) == 0:
                            c.privmsg(nick, "Aucun groupe d'enregistré.")
                            return
                        else:
                            number = 1
                    else:
                        number = arguments[2]
                        
                    if (RepresentsInt(number)):
                        tmp = int(number)
                        if ((tmp-1 >= len(find)) or (tmp <= 0)):
                            c.privmsg(nick, "Et faut pas me prendre pour une idiote ! Tu demandes un numéro de groupe que tu n'as pas ;)")
                            return
                        number = find[int(number)-1]
                    bool = False
                    for i in range(len(classe_url)):
                        if classe_url[i][0] == number:
                            text = parser_all_day(classe_url[i][1]+".xml", d)
                            bool = True
                            
                    if (len(text) == 0 and bool):
                        c.privmsg(nick, "Pas de cours pour " + t + " ... Lucky "+ nick +" ;)")
                        return
                    else:
                        bool = False
                        for i in range(len(text)):
                            if (d):
                                text2 = "Demain:"
                            else:
                                text2 = "Aujourd'hui:"
                            for j in range(len(text[i])):
                                text2 = text2 + " " +  str(text[i][j])
                                bool = True
                            c.privmsg(nick, text2)
                            
                        if not bool:
                            c.privmsg(nick, "Je n'ai pu trouver le groupe " + number + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")
                            return
                    

                elif arguments[1] == "now":
                    find = find_user_and_group(self.user_to_group, nick)
                    if (len(arguments) == 2):
                        if len(find) == 0:
                            c.privmsg(nick, "Aucun groupe d'enregistré.")
                            return
                        else:
                            number = 1
                    else:
                        number = arguments[2]
                    
                    if (RepresentsInt(number)):
                        if ((int(number)-1 >= len(find)) or (int(number) <= 0)):
                            c.privmsg(nick, "Je n'ai pu trouver le groupe " + number + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")
                            return
                        edt = find[int(number)-1]
                        for i in range(len(classe_url)):
                            if classe_url[i][0] == edt:
                                text = parser_delayed(classe_url[i][1]+".xml")
                                if len(text) == 0:
                                    c.privmsg(nick, "Plus de cours pour aujourd'hui ... Lucky "+ nick +" ;)")
                                    return
                                else:
                                    bool = False
                                    for j in range(len(text)):
                                        text2 = "Aujourd'hui: "
                                        for k in range(len(text[j])):
                                            text2 = text2 + " " +  str(text[j][k])
                                        c.privmsg(nick, text2)
                                        bool = True
                                    if not bool:
                                        c.privmsg(nick, "Je n'ai pu trouver le groupe " + edt + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")
                                    return
                        c.privmsg(nick, "Je n'ai pu trouver le groupe " + edt + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")

                    else:
                        for i in range(len(classe_url)):
                            if classe_url[i][0] == arguments[2]:
                                text = parser_delayed(classe_url[i][1]+".xml")
                                if len(text) == 0:
                                    c.privmsg(nick, "Plus de cours pour aujourd'hui ... Lucky "+ nick +" ;)")
                                    return
                                else:
                                    bool = False
                                    for j in range(len(text)):
                                        text2 = "Aujourd'hui: "
                                        print text, len(text)
                                        for k in range(len(text[j])):
                                            text2 = text2 + " " +  str(text[j][k])
                                            bool = True
                                        c.privmsg(nick, text2)
                                    if not bool:
                                        c.privmsg(nick, "Je n'ai pu trouver le groupe " + arguments[2] + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")
                                    return
                                    
                        c.privmsg(nick, "Je n'ai pu trouver le groupe " + arguments[2] + ". Vérifie que ce groupe existe bien en faisant \'!edt licence\' si c'est un groupe de licence, de même pour ceux de master et master2.")

                elif arguments[1] == "groups":
                    if len(arguments) > 2:
                        c.privmsg(nick, "Pas besoin de rajouter quelques choses après \'groups\' ;)")
                    find = find_user_and_group(self.user_to_group, nick)
                    for i in range(len(find)):
                        text = text + " {nmb}: ".format(nmb=i+1) + find[i] + " "
                    c.privmsg(nick, "Voici vos groupes : " + text)
             
                elif arguments[1] == "add":
                    if len(arguments) < 3:
                        c.privmsg(nick, "Il faut un identifiant de groupe à ajouter. Voyons ... ;)")
                    else:
                        for i in range(2, len(arguments)):
                            self.user_to_group = add_user_and_group(self.user_to_group, nick, arguments[i])
                            rewrite_user_to_group(self.user_to_group)
                            find = find_user_and_group(self.user_to_group, nick)
                        for j in range(len(find)):
                            text = text + " {nmb}: ".format(nmb=j+1) + find[j] + " "
                        c.privmsg(nick, "Voici vos groupes : " + text)

                elif arguments[1] == "delete":
                    if len(arguments) < 3:
                        c.privmsg(nick, "Il faut un identifiant de groupe à supprimer. Voyons ... ;)")
                    else:
                        for i in range(2, len(arguments)):
                            self.user_to_group = del_user_and_group(self.user_to_group, nick, arguments[i])
                            rewrite_user_to_group(self.user_to_group)
                            find = find_user_and_group(self.user_to_group, nick)
                        for j in range(len(find)):
                            text = text + " {nmb}: ".format(nmb=j+1) + find[j] + " "
                        c.privmsg(nick, "Voici vos groupes : " + text)
                
                elif ((arguments[1] == "help") and (len(arguments) == 2)):
                    text = "Voici la liste des commandes que je propose : " 
                    for i in range(len(edt_opt)-1):
                        text = text + edt_opt[i][0] + ', '
                    text = text + edt_opt[len(edt_opt)-1][0] + ' '
                    c.privmsg(nick, text)
                    c.privmsg(nick, "Faites précéder ces commandes du mot help pour mieux comprendre ce qu'elles font ;)")

                elif arguments[1] == "help":
                    text = ""
                    for i in range(len(edt_opt)-1):
                        if edt_opt[i][0] == arguments[2]:
                            text = edt_opt[i][0] + ": " + edt_opt[i][1]
                            break
                    if text == "":
                        text =  "Cette commande n'existe pas ... Essaie encore !"
                    c.privmsg(nick, text)
                
                else:
                    for i in range(len(classe_url)):
                        if classe_url[i][0] == arguments[1]:
                            text =  classe_url[i][0] + ": " + classe_url[i][1] + ".html "
                            c.privmsg(nick, text)
                            return
                    c.privmsg(nick, "Impossible de trouver le groupe " + arguments[1] + " ...")

            elif arguments[0] == "!joke":
                if ((len(arguments) > 1) and (arguments[1] == "add")):
                    joke = ""
                    for i in range(2, len(arguments)):
                        joke = joke + " " + arguments[i]
                    self.jokes.append([joke])
                    rewrite_jokes(self.jokes)
                    text = "Cette blague a bien été enregistrée \o/"
                else:
                    text = "La prochaine implémentation prendra en compte un dictionnaire de blagues dont TU seras un des auteurs. Bien sûr, celles-ci devront être \"approuvées\", mais il ne devrait pas y avoir de problèmes :) Pour ajouter une blague, faites-là précéder du mot clé \'add\' : \'!joke add Peut-on dire qu'un clavier azerty en vaut deux ?\'"
                c.privmsg(nick, text)


            else:
                c.privmsg(nick, "Commande non comprise : " + cmd)
                text = "Voici la liste des commandes que je propose : " 
                for i in range(len(command)-1):
                    text = text + command[i] + ', '
                text = text + command[len(command)-1]
                c.privmsg(nick, text)
                c.privmsg(nick, "Si vous ne savez pas comment l'utiliser, faites-là suivre de help : \'!edt help\'")
    
        except:
            c.privmsg(nick, "Oups, une erreur est survenue. Pouwapouwa s'en chargera dès que possible !")
            file = open("log/errors", 'a+')
            file.write("\n" + strftime("%d/%m/%Y  %H:%M", gmtime()) + " : " + nick + " " + cmd + "\n")
            file.close()
            #pass
            raise 



def main():
    import sys

    server = "chat.freenode.net"
    port = 6667
    channel = "#testpouwapouwa"
    nickname = "powpow-beta"

    bot = TestBot(channel, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
