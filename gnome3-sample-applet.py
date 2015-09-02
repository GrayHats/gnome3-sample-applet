import os
import signal
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import GLib as glib
import _thread
import subprocess

APPINDICATOR_ID = 'tps'
indicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_INFO, appindicator.IndicatorCategory.SYSTEM_SERVICES)
p = subprocess.Popen("ps -eo pid,command | grep 'tomcat' | grep -v grep | awk '{print $1}'", stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
pid = output.decode("utf-8").replace("\n","")

def main():
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    indicator.set_label(pid, '')
    _thread.start_new_thread(update_ind_label, ())
    gtk.main()

def update_ind_label():
    value = glib.timeout_add_seconds(5, handler_timeout)

def handler_timeout():
    p = subprocess.Popen("ps -eo pid,command | grep 'tomcat' | grep -v grep | awk '{print $1}'", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    pid = output.decode("utf-8").replace("\n","")
    indicator.set_label(pid, '')
    return True

def build_menu():
    menu = gtk.Menu()
    item_kill = gtk.MenuItem('Kill')
    item_kill.connect('activate', kill)
    menu.append(item_kill)
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def kill(source):
    k = subprocess.Popen("kill -9 "+pid, stdout=subprocess.PIPE, shell=True)
    (output, err) = k.communicate()
    indicator.set_label('NA', '')

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
