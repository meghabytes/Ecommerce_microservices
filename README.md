First step - create a python virtual environment. 


meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ python3 -m venv tutorial-env
The virtual environment was not created successfully because ensurepip is not
available.  On Debian/Ubuntu systems, you need to install the python3-venv
package using the following command.

    apt install python3.10-venv

You may need to use sudo with that command.  After installing the python3-venv
package, recreate your virtual environment.

Failing command: /home/meghana/Cloud/Understanding_micro/tutorial-env/bin/python3

meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ 
 *  History restored 

meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ python3 -m venv tutorial-env
meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ source/bin activate
bash: source/bin: No such file or directory
meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ source tutorial-env/bin/activate
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ 


export FLASK_APP=hello
flask run


(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro/src$ python app.py
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro/src$ python app.py
 * Serving Flask app 'app'
 * Debug mode: off
Permission denied
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro/src$ python app.py
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.2:5000
Press CTRL+C to quit
192.168.1.2 - - [30/Mar/2024 09:54:39] "GET / HTTP/1.1" 200 -
192.168.1.2 - - [30/Mar/2024 09:54:39] "GET /favicon.ico HTTP/1.1" 404 -

Running in port 90 gave permission denied.



(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ docker run -d -p 80:5000 --name web webapp:1.0
3c4b03dd9d21b8696605af55cccdd7e8959551e640eb5bb374918471660a58d3
docker: Error response from daemon: driver failed programming external connectivity on endpoint web (edcc20efbb28e0c43ddb8a640454344859f2fb854b61695db3a71706de6afd90): Error starting userland proxy: listen tcp4 0.0.0.0:80: bind: address already in use.
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ docker run -d -p 86:5000 --name web webapp:1.0
docker: Error response from daemon: Conflict. The container name "/web" is already in use by container "3c4b03dd9d21b8696605af55cccdd7e8959551e640eb5bb374918471660a58d3". You have to remove (or rename) that container to be able to reuse that name.
See 'docker run --help'.
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ docker run -d -p 86:5000 --name webb webapp:1.0
3f4ae70284ff0e2a82e59529c61579af6dd687b270d2ce5a6c8244257641b783
(tutorial-env) meghana@meghana-Lenovo-IdeaPad-S145-15IIL:~/Cloud/Understanding_micro$ 