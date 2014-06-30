sublime-wrangler
================

Wrangler support for sublime text

## Prerequisite

* Download and compile/install wrangler (http://www.cs.kent.ac.uk/projects/wrangler/Home.html)
* Add wrangler to your libs folder in your erlang install folder  
* Add erl_interface to your path(C:\Program Files\erl5.10.3\lib\erl_interface-3.7.14\bin)
* Start a erlang node with the name of wrangler and the application wrangler (erl -sname wrangler -eval "application:start(wrangler)")

## Installation

* clone this repository into the ST `Packages` folder

## How does it work

Sublime Text and the erlang node communicate through rpc calls with erl_call, Sublime expect the node the have the name "wrangler"
The wrangler node will hold a command log and be able to support undo on the processed commands.
The command log is totally seperated from sublime's command log.

## Features

The following feature is exposed throught the context menu

* Export - Select a function and export
* Rename Variable - Select a variable and rename it.
* Rename Fun - Select a function and rename it
* Rename Mod - Rename a module
* Undo - Undo the last refactoring command on the wrangler node.

## Status

The plugin is still early stage, help is very welcomed.
