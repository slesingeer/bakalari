#!/usr/bin/env python3
"""Žákovka – průměry, cíle, absence, rozvrh, úkoly.
Spuštění: python bakalari_app.py   (jen standardní knihovna, Python 3.8+)
Heslo se nikam neukládá."""
import os, hmac, base64, hashlib, secrets, json, datetime, socket, urllib.error, urllib.request, urllib.parse, webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

# Lokálně běží jen na tomto počítači. Na hostingu (proměnná PORT) se otevře do internetu,
# ale jen s přístupovým heslem v proměnné APP_PIN.
HOST = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")
PORT = int(os.environ.get("PORT", 8765))
PIN = os.environ.get("APP_PIN", "")
ICON = "iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIAAAB7GkOtAAAr9klEQVR42u3deZRU9Z338e+9tXU3yCKKiASCgKC4g4D7kqhRH7dRg7ssaoyGQXBOJrOeZ2ZOZvJkkrSI4hJ1bEBQIhqVqKMxUeMSt0AAQUFQEGWXvamquz1/NEh3U1W3uqpu963vfX/+yjmp07S/Q70+RfWvP2VcdPFmKSKGSLkPM8r/aob/Y4zAvv/mDzMq8ZD2OLEiHpbnO233EyvmqxnhODHfhxmhOTG/hzX7Yzr0xIr5akY4TqzN3nTcifn+HTNM9Ed/9Ed/9I+g/iJiBn5k6I/+6I/+6B8+/f0LAP3RH/3RH/1V6u9TAOiP/uiP/uivVf9CBYD+6I/+6I/+ivXPWwDoj/7oj/7or1v/3AWA/uiP/uiP/ur1z1EA6I/+6I/+6B8F/VsXAPqjP/qjP/pHRP8WBYD+6I/+6I/+0dF/XwGgP/qjP/qjf6T031MA6I/+6I/+6B81/UXERH/0R3/0R/8I6m8UswWE/uiP/uiP/vr0l3LH4NAf/dEf/dG/OvWXssbg0B/90R/90b9q9ZfSx+DQH/3RH/3Rv5r1lxLH4NAf/dEf/dG/yvWXUsbg0B/90R/90b/69Zc2j8GhP/qjP/qjvwr9pW1jcOiP/uiP/uivRX9pwxgc+qM/+qM/+ivSX4odg0N/9Ed/9Ed/XfpLUWNw6I/+6I/+6K9Of/Efg0N/9Ed/9Ed/jfqLzxgc+qM/+qM/+ivVv+AYHPqjP/qjP/rr1V/yFgD6oz/6oz/6q9Y/TwGgP/qjP/qjv3b9cxUA+qM/+qM/+kdA//0KAP3RH/3RH/2joX/LAkB/9Ed/9Ef/yOjfrADQH/3RH/3RP0r67y0A9Ed/9Ed/9I+Y/iJioj/6oz/6o38E9RejyDE49Ed/9Ed/9NelvxQ1Bof+6I/+6I/+6vQX/zE49Ed/9Ed/9Neov/iMwaE/+qM/+qO/Uv0LjsGhP/qjP/qjv179pZgCQH/0R3/0R399+vsXAPqjP/qjP/qr1N+nANAf/dEf/dFfq/6FCgD90R/90R/9FeuftwDQH/3RH/3RX7f+uQsA/dEf/dEf/dXrn6MA0B/90R/90T8K+rcuAPRHf/RHf/SPiP4tCgD90R/90R/9o6O/5B+DQ3/0R3/0R3/N+kueMTj0R3/0R3/0V66/5BqDQ3/0R3/0R3/9+u8/Bof+6I/+6I/+kdBfWhYA+qM/+qM/+kdF/+YFgP7oj/7oj/4R0v+bAkB/9Ed/9Ef/aOnfVADoj/7oj/7oHzn9RYwitoDQH/3RH/3RX53+4r8FhP7oj/7oj/4a9RefLSD0R3/0R3/0V6q/FNoCQn/0R3/0R3+9+kveLSD0R3/0R3/0V62/5N4CQn/0R3/0R3/t+kuOLSD0R3/0R3/0j4D++20BoT/6oz/6o3809JcWBYD+6I/+6I/+kdG/WQGgP/qjP/qjf5T031sA6I/+6I/+6B8x/UXERH/0R3/0R/8I6i+GmOiP/uiP/ugfQf1FxAz0yNAf/dEf/dE/nPqL/xgc+qM/+qM/+mvUX3zG4NAf/dEf/dFfqf5SaAwO/dEf/dEf/fXqL3nH4NAf/dEf/dFftf6SewwO/dEf/dEf/bXrLznG4NAf/dEf/dE/Avobkuf3ANAf/dEf/dFft/5STAGgP/qjP/qjvz79/QsA/dEf/dEf/VXq71MA6I/+6I/+6K9V/0IFgP7oj/7oj/6K9c9bAOiP/uiP/uivW38pawwO/dEf/dEf/atWfyl9DA790R/90R/9q1l/KXEMDv3RH/3RH/2rXH8pZQwO/dEf/dEf/atff2nzGBz6oz/6oz/6q9Bf2jYGh/7oj/7oj/5a9Jc2jMGhP/qjP/qjvyL9ix6DQ3/0R3/0R39d+ktRY3Doj/7oj/7or05//wJAf/RHf/RHf5X6+xQA+qM/+qM/+mvVv1ABoD/6oz/6o79i/fMWAPqjP/qjP/rr1j93AaA/+qM/+qO/ev1zFAD6oz/6oz/6R0H/1gWA/uiP/uiP/hHRv0UBoD/6oz/6o3909N9XAOiP/uiP/ugfKf33FAD6oz/6oz/6R01/ETHRH/3RH/3RP4L6G4b/FhD6oz/6oz/6K9Rf/LaA0B/90R/90V+n/oULAP3RH/3RH/3V6l+gANAf/dEf/dFfs/4iEkd/9C9T/77fNn/y73WpmiK/naKyYplz/y93b9vqVZf+g4fGbr6zplPnSh7FqhXu3f+x28qiP/pXnrLYUUP+Hv3Rv5zX/tu2emtWuyNOTRiVc+/AHuaIUxPLP3a2bfGqRf+zv5cYc0dNZYtwyybvnv9M796F/ugfCGWtCgD90b+UP3H9Wnf3bjn6+HgF7aupNU4+I7Flk7dmlRty/eMJuf7W1PmXJg2zggcg6bQ39afpTRs89Ef/gChrXgDoj/6l/4krlztdu5rfHhCroICxmJwwIl7byVi6yPG8kOrftbsx4Se1R59YyfITEdeVX9dnVi5z0R/9g6PsmwJAf/Qv98QWL7QPHxTreUhFXwaLHD4oNnBIfOF828qGTv/DB8Um/nNtr94V/k8Wkacash+8ZaM/+gdKmYn+6F+pE3MdeaA+/dUat+IaDjk69k//WXdYv1io9D/l7MSd/1rbtZtR8f/e11+2Xn/ZQn/0D5qy2FFDfoL+6F+pE7MtWTTfGXlqorI/CxWRuk7GyWfE16/11n7pdrj+Zkyuuil1yeikWfmX/rJkgTPj/oznoT/6B02ZERs65Cfoj/4VPLHGRu/TT5xRpydilfxxgIhIPG4MGxWPx2TZEqcD9e/cxbj9x7XDRlX4Tf+mfPWFO+3/ZSwL/dE/cP2Npn8BoD/6V/bEtmz2Nq5zTxxZyYuh3/yJg46M9e1vLprv2HYH6N+nn3nnv9T16RfAK3+R7Vu9KT9N79zuoT/6t4P+UkwBoD/6l3BiX37hep4MGRrIy+RDepsnjIgvXejs2um1p/7DT4nf9ne1nbsYQfxHWVm572fpdV+iP/q3k/7+BYD+6F/yiS1b6vTsZfbpV+l3gprehznAGHVGfM0qd8M6rx0sMwy59OrkVTemYoE0mniePHZf5uNFDvqjf7vp71MA6I/+ZZ7Yor/YQ4bGDzwokDdMEgljxKkJ25ZPP3ECtay2zrh1cu3JZyUksDw/J/vWqzb6o3976l+oANAf/cs/MdeVv35oDxsZr+w8TvNv5shjYoceZi5eYLtOECcmvQ4z7/yX2v4DA/l3TFP+/Ib9zONZ9Ef/dtZf8q2Boj/6V+rEdu7w7vnZ7sZdXnCADj85/uN/qzvwIKPSJybHnBj/8X/U9uxlBvfNL1/qzH44g/7o3/765/4XAPqjf2VPbOcOb9UKZ8RpCTMwSLt2M0aenvh8hbt5o1eREzMMueDy5LW3pBIJQwLLxnXu1P/KWGn0R/8O0D9HAaA/+gdxYps2eNu2eMcND+ZHqCIikkwZI09L7Nrlfb7CLfPEkilj3ISaM8+r/DXW5mnc6d3z08y2r72y/mKgP/qX8ZAWBYD+6B/cia3+zE3VGAMHB/hmumHK0SfED+xhfLTQcd0ST+ygnubEf6494qgAv08RcRx54BeZNZ+5ZR0s+qN/eQ/ZVwDoj/5BnpiIyNJFTp++sUMPC/AtdRH5Vv/YkcfEFs93Muk2n9jgo2N/+4+1PQ4O9jsUkVkPZRZ94JR1sOiP/mU/xER/9G8f/UVEPHnk3vSqlY4EnP6DYv/4X3X9B8badGLnXJCY8A+1AV1Yap6Xn7XefcNGf/TvWP3FfwwO/dG/ot+/48iiv9jDT07U1gXrbE2tMer0xNYt3prPXd8TSyTkhttqzrskaQSOv8x/157zaBb90b/D9ReRgmNw6I/+AXz/6bR88pE96oxEPB4st2ZMjhse79TZWLq42efJ7PeNdTvQmPAPdUOPD/ZN/6asWuE+9Mu045RxsOiP/hXS3yhUAOiP/oE9M7dv9b5a7Z50SqIdXnH3HxgbNDi2eL6Tzeb4xgYMjk38p9pDegf+pr+IbNnkTd37Ab/oj/4drn/+fwGgP/oH/Mxcv85L7/aGHhfgxdBv0qOnOWxUfNkSZ/s2r/k3duo5ifETa4J+M2rvv3u8e/d+wC/6o38Y9M9TAOiP/kE/Mw1DRFYud7t0NSr7McL5UtfJGHV6YuM6d+0aV0TiMRk9NnXxVUmzPV76i+vKI3s/4Bf90T8k+ucqAPRH/3bRvylLFjqHD4odfEh7MByLy4mj4vGErFvj3v7j2hNGtsc/Ppoyd3r2/bfsMk4M/dG/8vqLiHHVZVvQH/07RP+m/1VbZ/z9v9ce2qddXoqLiIhtSTzRbn+avPGy9ZvHsmWcGPqjfyD6S4sxOPRH/3bXX0R2N3r3/jy9Y3uAa3Gt0p76L1ngzJ2O/ugfRv2bFQD6o39H6N+UTRvcab9IW5Yoy9ov3EfvybhuySeG/ugfoP57CwD90b/j9G/KymVOw/1pr/3+GRB4dmzzHvjvdCbtoT/6h1N/ETHRH/07XP+mvP+2Pe+prKiIZclDv0x/vQn90T+8+ovR7GcA6I/+Hah/U+bNzb77pi1VHs+TGdMyn3/qoj/6h1l/KWoMDv3Rv130b8qMB9MrPgl8LS7QzJuTnf+ujf7oH3L99xQA+qN/SPQ3RGxL7v9FetMGV6oz775hv/yshf7oH379RcREf/QPj/5N2bnDu/dn6UA/RjigfPqxM/vhDPqjf1Xob+T7UHj0R/+O0r8p675yH6pPu1X1VtDG9e6vf5VxbPRH/+rQX4opAPRH/3bWvykfL3ZmPZqpFv0bd3kP/DzTuNNDf/SvFv39CwD90b9D9G/Km69ar8yrgl8Pcxx5uD6zYa2L/uhfRfr7FAD6o38H6t+Upx/PLHg/7BdDn3g4s3yJg/7oX136FyoA9Ef/DtdfRDxP/ufe9OrPwnsp6JXnrD+/bqM/+led/nkLAP3RPwz6Nz0sm5FpP9+99eswXgpa8J79/JNZ9Ef/atQ/dwGgP/qHR/+mbNviTfvv3ZlMuDpg9Up3+rRMgf0i9Ef/MOsvIsb3L9+C/ugfZv0rZ5kRjhNDf/QPhf6t/wWA/uiP/uiP/hHRv0UBoD/6oz/6o3909JeyxuDQH/3RH/3Rv2r1l9LH4NAf/dEf/dG/mvWXEsfg0B/90R/90b/K9S9pDA790R/90R/9q19/afMYHPqjP/qjP/qr0F/aNgaH/uiP/uiP/lr0lzaMwaE/+qM/+qO/Iv2l2DE49Ed/9Ed/9NelvxQ1Bof+6I/+6I/+6vQX/zE49Ed/9Ed/9Neof44CQH/0R3/0R/8o6C+FxuDQH/3RH/3RX6/+kncMDv3RH/3RH/1V6y+5x+DQH/3RH/3RX7v+kmMMDv3RH/3RH/0joL+0HoNDf/RHf/RH/2jo33IMDv3RH/3RH/0jo7/sKwD0R3/0R3/0j5L+ewsA/dEf/dEf/SOmv4jE0V+l/omETJt5gBBSifzrD9K7Gz30V6a/GIYZjiND/wBfyRISdNC/GvUX/y0g9Ed/QtBfo/7iswWE/uhPCPor1V8KbQGhP/oTgv569Ze8W0DoX+X6UxIE/dFf/IYeTPRHf0LQP4L6S44tIPRHf0LQPwL6S+stIPRHf0LQPxr6GwU+FB790Z8Q9FesvxRTAOiP/oSgvz79/QsA/dGfEPRXqb9PAaA/+hOC/lr1L1QA6F/d+hv0AmnXZkD/qtM/bwGgP/oTgv669ZeyxuDQH/0J+qN/1eovpY/BoT/6E/RH/2rWX0ocg0P/0OtPDxD0R3/fL2UGcGToj/4E/dE/7PpLm8fg0B/9Cfqjvwr9pW1jcOiP/gT90V+L/tKGMTj0R3+C/uivSP+ix+DQH/0JQX9d+ktRY3Doj/6EoL86/f0LAP3RnxD0V6m/TwGgP/oTgv5a9S9UAOiP/oSUURLoH3b98xYA+qM/IeivW//cBYD+6E8I+qvXP0cBoD/6E4L+UdC/dQGgvxr9KQmC/ugvbRiDQ3/0JwT9I6P/vgJAf/QnBP0jpf+eAkB/9CcE/aOmv4iY6I/+hKB/BPU3jCLH4NAf/QlBf136S1FjcOiP/iTC2bHNs7Ie+uvT378A0B/9SZRjWzL97qxto79C/X0KAP3Rn0Q8Tz2SXb3CRX+V+hcqAPRHfxLxvDbPnv+2g/5a9c9bAOiP/iTiWTrfeek3Fvor1j93AaA/+pOIZ/2X7uz7s+Khv2b9cxQA+qM/iXgad3qP1WezafRXrn/rAkB/NfpTEqS0OI7MmJrdssFDf/X6tygA9Ed/Qp6dbn221EX/KOgvInH0V6m/ZckPr95ZxIkV89WMcJxYm8EJ5u9Y66RqjIn/N9WrjynVn7dfsd/7o43+EdF/z78A0F/na3/0D/7EDENuuCOpQ/9PP3LnzbLQPzr6i4iJ/uiP/iWf2EWjE0edEFOg/+b13qx7s66D/hHS3/CbgkB/9Ef/vBl2avyc/5NQoH96tzz2q0zjLg/9I6W/FCwA9Ed/9M+bfgPM0TcnFejveTL7vuzGtegfOf0LFAD6oz/6503X7sbYSam4hlf/8sJs65OFDvpHUP98BYD+6I/+eZNIyvjJqS7dNNy2/fBPzp9estE/mvrnLAD0R3/0L5Rrbk316a/h2s+q5e7T/5NF/8jqv38BoD/6o3+hnHdZ4vhRGq79bN3szZiSdWz0j67+rQoA/dEf/QvlmOGx86/Q8MZ/NiPT67M7t3voH2X9mxcA+qM/+hdK777mdT9MGdX/zr/nyZyHsl+tdtE/4vp/UwDoj/7oXyiduxjj70olUwpe/cvvn7EWv++gP/o3FQD6oz/6F0osLmPvTHXvoeHaz6L3nD88a6M/+jf9/6agP/qjf8FcNS7Z/wgN136+/Nyd81DW89Af/ff8/yb6oz/6F8iZF8RHnBFXoP+Obd70u7NWFv3RX75548dEf/RH/3wZcmzs4ms07D3YtsyYkt32tYf+6N/8bX8T/dEf/XOm56HmjT9Kmhre+5GnH82u/tRFf/Rv9UNfE/3RH/33T20nY/xdqZo6DT/4feMF+y9vOuiP/vtf+THRH/3Rv1VMU26akDy4lwb9P17gvPikhf7on/PCp4n+6I/+rXLp9ckjjtaw97DhS2/2/U3XftAf/QtvAaE/+qO/yKiz46efp+HaT+Mu77H6TGY3+qN/3l/2MtEf/dH/mwwYYl4xRsO1H9eRx+/Jfr3BQ3/0F58tIPRHf/QXOfBgY8zEVEzDez/y3ExrxVIX/dFffLaA0B/90V8kVSM335XqdICGH/y+86r951dt9Ed/3xMz0R/90d8w5PrbU736aLjzv2KJ+/xMC/3Rv5gTM9Ef/SOuv4hc9P3E0BM1vPWzeYP3+NSs66A/+hd1YqagP/pHW/9hp8TPuVjDx7xkdktDfaZxVxFHgf7o31QA6I/+Uda/3wBz9C0arv14nsy+P7vhS/RH/zacmBnYkaE/+odd/67djbGTUnENr/7lxSetjxe46I/+bToxM5gjQ3/0D7v+yaSMm5zq0k3DtZ8P33TeeMFBf/Rv64mZ6I/+EdTfEBl9S+pb/TVc+1n9qfvMoxb6o38JJ2aiP/pHUP/vXpo44WQN1362fe1Nn2LZNvqjfyknZqI/+kdN/6OHxb53pYY3/q2sNNRbO7d56I/+pZ2Yif7oHyn9D/2Wee0PU0b1v/PveTLnQeurVS76o3/JJ2aiP/pHR//OXYxxk1OpGgWv/uXV39qL3nfQH/3LOTET/dE/IvrHYnLTxNSBB2u49rPofefV39roj/5lnpiJ/ugfBf1F5IqxycMHa7j289Vqd86DluehP/qXe2JmwM9M9Ef/UOh/xvfiI8/S8DEvO7d5Db+yrCz6o38FTswM8pmJ/ugfCv0HHxO7+FoNew+2LdOnWNu+9tAf/StyYqagP/qr1v/gXsYNE5Kmhvd+5JlHrdWfuuiP/pU6MRP90V+x/rV1xvi/q6mt0/CD3zdesD9800F/9K/giZkBPDPRH/1Dob9pyg0Tkgf30qD/JwvdF5+00R/9K3tiZqWfmeiP/qHQX0QuuS45+BgNew8bvvJm3Zdtfu0H/dG/IidmVvSZif7oHxb9R54VP/18Ddd+Gnd5DfXZzG70R//Kn5hZuWcm+qN/WPQ/fLB5xRgN135cRx6fam1e76E/+gdxYmaFnpnoj/5h0b/7QcZNE1MxDa/+5fmZ1oolLvqjf0AnZlbimYn+6B8W/VM1Mn5yqnMXDT/4ffcPzjuvOuiP/sGdmFn2MxP90T8s+huGXPvD1KF9Ndz5X7nUfW6Ghf7oH+iJmeiP/jr0F5ELrkocPUzDtZ+vN3gzp1qOg/7oH+yJmeiP/jr0P+Hk2Hcu0fAxL5m0NNRnG3d66I/+QZ+Yif7or0D/b/U3R9+SUqC/58kT07Lrv0R/9G+PEzPRH/2rXf8u3Yxxk1MJDdc+5aU59tIFLvqjf/ucmIn+6F/V+scTMnZSqkt3Ddd+5r/tvP47G/3Rv91OzER/9K9e/UVk9C3JvgM0XPv5YoU792EL/dG/PU/MRH/0r179v3NJ4sRTNPzG1/Yt3vS7LdtGf/Rv1xMz0R/9q1T/oSfGLrhKw7UfKysN9daObR76o387n5iJ/uhfjfr36mNed3vK0PDOv/zm19aXn7voj/7tf2Im+qN/1enf6QBj/F2pVI0G/V991l74roP+6N8RJ+Y/Bof+6B8u/WMxGTMxdeDBGl78L/7A+f3TNvqjf4foL35jcOiP/uHSX0T+Zkzy8CEarv2sXe3NedDyPPRH/47RXwqOwaE/+odO/9PPj486W8O1n53bvYb6bDaD/ujfYfpL/jE49Ef/0Ol/xNGxS67T8Pu+ji0zplhbN3voj/4dqL/kGYNDf/QPnf4H9TJunJA0Nbz3I888Zq1a7qI/+nes/pJrDA790T90+tfUGePvStV20vCD3z+9ZH/whoP+6N/h+st+Y3Doj/6h09805YYfJXsequHF/7KF7otP2OiP/mHQX1qOwaE/+odOfxG5+NrkkGM1fMzLxrXerGlZz0V/9A+F/tJsDA790T+M+o84M37G9zRc+9m9y2uoz2Ya0R/9w6L/N2Nw6I/+YdS//2DzyrEarv24jjx+r7V5nYf+6B8e/UXERH/0D6f+3XsYYyamYhpe/cu8WdaKj1z0R/9Q6S9imOiP/iHUP5mScXelOnfRcO3nvdecd15x0B/9w6a/iP8WEPqjf3vrbxhy7W2p3n01XPtZ+bH7XIOF/ugfQv3FbwsI/dG/vfUXkfOvSBxzkoZrP19v9GZNtRwH/dE/jPpLwS0g9Ef/DtD/+FGxcy/T8DEvmbRMr8/u2uGhP/qHU3/JvwWE/ujfAfr36W9efWtKgf6eJ08+kF2/Bv3RP7z6S54tIPRH/w7Q/4CuxrjJqYSGa5/y8m/spX9x0R/9w6y/5NoCQn/07wD94wkZNznVtbuGaz8L3nZem2ejP/qHXH/ZbwsI/dG/A/QXke/fnOw7QMO1ny9WunMfsdAf/cOvv7TcAkJ/9O8Y/c+5ODHsVA2/8bV9izfjbsu20B/9q0B/abYFhP7o3zH6Dz0xduH3NVz7sbIy425rx1YP/dG/KvQ3CvwiGPqjfzvo36uPed3tSUPDO/8y92FrzWcu+qN/tegvxRQA+qN/QM/MTp2NcZNTqRoN/P/xOfuvf3bQH/2rSH//AkB/9A/omRmLyU0Tkz16atB/yYfOK3Nt9Ef/6tLfpwDQH/2De2ZeflNywJEa9h7WfeE9+aDleeiP/lWmf6ECQH/0D+6Zedq58ZPP0XDtZ9cOr6E+m02jP/pXn/55CwD90T+4Z+agobFLr9fw+76OLTOnWFs3eeiP/tWof+4CQH/0D+6ZedAhxo0TkqaG937ktw3W58tc9Ef/KtU/RwGgP/oH98ysqTPG35Wq66zhB79v/a/9wesO+qN/9erfugDQH/2De2YahtxwR7Jnbw17D8sWuS/MttEf/ata/xYFgP7oH+gz8+Jrk0OO0/DWz8a13uz7LNdFf/Svbv33FQD6o3+gz8yTzoifeYGGaz/pRm96fTbd6KE/+le7/nsKAP3RP9Bn5rcHmVeN03Dtx3Vl1r3WpnXoj/4a9BcRE/3RP9BnZvcexthJqZiGV//yu1nW8sUu+qO/Dv0No8gxOPRH/5IelkzJuMmpzl00XPt5/zXn7Zcd9Ed/NfpLUWNw6I/+JT3MMOSa21K9+2m49vP5J+6zDRb6o78m/f0LAP3Rv+SHnf83yWNP0nDtZ8smb+Y9luOiP/qr0t+nANAf/Ut+2PEj49+9TMMb/9m0TK/P7trpoT/6K9O/UAGgP/qX/LA+/WNX/0DDx7x4njz5QHbdGvRHf4X65y0A9Ef/kh/WpZs5blIyoeHap7wy114y30V/9Fepf+4CQH/0L/lhiYQx5s5k1wM1XPv56zvOH5+30R/9teqfowDQH/1LfphhGFeOT/YbqOHaz5qV7lOPWOiP/or1b10A6I/+5eh/9kXx4adpuPazfYs3Y4plW+iP/pr1b1EA6I/+5eh/5PGxC0cnFOhvWzJjirV9q4f+6K9b/30FgP7oX47+hxxmXHe7hms/IjL3EWvNZy76o796/fcUAPqjfzn613U2xk1O1dRq0P+Pz9sL3nHQH/2joL+ImOiP/uXob8bkxgnJHj01vPhfOt99Za6N/ugfEf0NKXMMDv2jrb+IXHZDYuBRGq79rFvjPfFA1vPQH/2jor+UNQaH/pHX/5Tvxk/5joa9h107vOn12Wwa/dE/QvpL6WNw6B95/QceZV52vYZrP44jj0+1tmzy0B/9I6W/lDgGh/6R179HT+PGCUlTw6V/ebbB+uwTF/3RP2r6SyljcOgfef1ramXc5FRdZw0/+H37Fef91x30R/8I6i9tHoND/8jrbxhy3e3JQw7ToP/yxe7vZlnoj/7R1F/aNgaH/pHXX0Quujpx5PEa3vrZtN6bdZ/luuiP/hHVX9owBof+6C8y/LTYWRdquPaTbvSm12fTjR76o39k9Zdix+DQH/1F+g00rxyvYebfdWX2NGvjWvRH/0jrL0WNwaE/+ot062GMuTMZ1/DqX154wl62yEV/9I+4/uI/Bof+6C+SSMrYSckDumr4we8Hbzhv/a+N/uiP/uIzBof+6C9iGHLND5KH9dOw9/D5Mve3DRb6oz/67ykA9Ef/AvqLyLmXxY8doeHaz9ZN3sx7LMdGf/RH/z0PM9Ef/Qvof+yI2LmXa9h7yGak4e7srh0e+qM/+kuhMTj0R38REendz7zmBxo+5sXzZM6D1rov0B/90b/Fw0z0R/+c+h/Q1Rg3KZnQcO1Tfv+0/dGHDvqjP/pLoTE49Ed/ERGJx2XMncluPTRc+1n4rvOH52z0R3/0l0JjcOiP/ntz5bhkv4Earv2s+cx96mEL/dEf/aXQGBz6o//enHVhfPjpGq797NjqzZhiWVn0R3/0LzAGh/7ovzdDjotddLWGaz+2JTOmWNu3eOiP/uiffwwO/dF/bw7pbVx/h4ZrPyIy9xHri5Uu+qM/+hf4ZS8zHEeG/h2vf11nY+zkVE2tBv1fm2cveMdBf/RH/8K/6muG4MjQv+P1N2Nyw4+SBx2i4cX/0vnuy0/Z6I/+6O879GCiP/qLyGXXJwYN1XDtZ/0a78kHsp6H/uiP/v5/jIn+6H/yOfFTvqth6Llxp9dwdzaTRn/0R3//P8Yo8KHw6B8R/QccaV52o4ZrP44jM6daWzZ66I/+6F+M/lJMAaC/Yv179DRu+ttkTMOlf3luuvXZxy76oz/6F6m/fwGgv2L9UzUydnKyrrOGH/y+83vnvdcc9Ed/9C9ef58CQH/F+huGXHd7stdhGn7w++lH7rxZFvqjP/q3Sf9CBYD+ivUXkQtHJ446QcNbP5vXe7Pus1wH/dEf/dumf94CQH/d+g87NXb2RRqu/aR3S0N9dvcuD/3RH/3bqn/uAkB/3fr3HWBedbOGmX/Xldn3ZTeuRX/0R/9S9M9RAOivW/+u3Y2xk5JxDa/+5cUn7WWLXPRHf/QvTf/WBYD+uvVPJGXspOQBXTVc+/nwT86bL9noj/7oX7L+LQoA/XXrLyJX35rs01/DtZ9Vy91nHrPQH/3Rvxz9pawxOPSvKv3PvTx+3EgN1362bvZm3mO5NvqjP/qXpb+UPgaH/lWl/zHDY+ddrmHvIZuR6Xdnd2330B/90b9M/aXEMTj0ryr9e/c1r7lNw8e8eJ7Mechatxr90R/9K6C/IRIP4MjQP0T6d+5ijJucTKYUvPoXw5DrJyRENPxTpkqz5D336Qftsv/Gon8o9Jc2j8Ghf1XpH4vLmInJbj0MIaTdehr9q0R/adsYHPpXlf4icuXY5LePMIUQ9Ef/XA8zK3dk6B8u/c+8IH7SGTEhBP3RP8/DzAodGfqHS/8hx8Yuupr3ygn6o3+hL2VW4sjQP1z69+xtXH9HwuS9H4L+6F/wYWbZR4b+4dK/tpMxblKqpo4f/BL0R3+fh5nor0l/MyY3Tkge1Av9Cfqjv//DTPRXo7+IfOeS+KChvPVD0B/9i3qYif5q9BeRHgejP0F/9C/2YSb6q9GfEPRH/zY9zER/9CcE/SOov7Qeg0P/atafiiDoj/5tepiJ/uhPSAXbAf2rRX/ZVwDoj/6EoH+U9N9bAOiP/oSgf8T0FxET/dGfEPSPoP5iFDkGh/7oTwj669JfihqDQ3/0JwT91ekv/mNw6I/+hKC/Rv3FZwwO/dGfEPRXqr8UGoNDf/QnBP316i95x+DQH/0JQX/V+kvuMTj0R39CSvuriP7Vo7/kGIND/2rWn5Ig6I/+xZ+Yif7oT0hlmwH9q0J/Q8Qs+suhP/oTgv569JdiCgD90Z8Q9Nenv38BoD/6E4L+KvX3KQD0R39C0F+r/oUKAP3RnxD0V6y/FByDQ3/0JwT91eov+cfg0B/9CUF/zfpLnjE49K9a/WkGgv7oX/RXM9Ef/QlB/wjqL/uNwaE/+hPSLn9j0b+j9ZeWY3Doj/6EoH9U9JdmY3Doj/6EoH+E9Je9Y3Dor0F/ioCgP/q36auZ6I/+hHRwSaB/x1BmmOE4MvRHf4L+6N+u+ovPFhD6oz8h6K9U/0IFgP7oTwj6K9Y/bwGgP/oTgv669c9dAOiP/oSgv3r9RcS4/eqd6K9Vf6OIL28U9x1U+G+2Uaknbxg+o9wIx4kV89UM4VPd0T/fvwDQH/3RH/3RPyL6tygA9Ed/9Ed/9I+O/vsKAP3RH/3RH/0jpf+eAkB/9Ed/9Ef/qOkvIib6oz/6oz/6R1B/wxAT/dEf/dEf/SOov0gRBYD+6I/+6I/++vT3LwD0R3/0R3/0V6m/TwGgP/qjP/qjv1b9CxUA+qM/+qM/+ivWP28BoD/6oz/6o79u/XMXAPqjP/qjP/qr1z9HAaA/+qM/+qN/FPRvXQDoj/7oj/7oHxH9WxQA+qM/+qM/+kdH/30FgP7oj/7oj/6R0n9PAaA/+qM/+qN/1PQXERP90R/90R/9I6i/IWWOwaE/+qM/+qN/deovZY3BoT/6oz/6o3/V6i+lj8GhP/qjP/qjfzXrLyWOwaE/+qM/+qN/lesvpYzBoT/6oz/6o3/16y9tHoNDf/RHf/RHfxX6S9vG4NAf/dEf/dFfi/7ShjE49Ed/9Ed/9FekvxQ7Bof+6I/+6I/+uvSXosbg0B/90R/90V+d/uI/Bof+6I/+6I/+GvUXnzE49Ed/9Ed/9FeqvxQag0N/9Ed/9Ed/vfrnH4NDf/RHf/RHf9X6S+4CQH/0R3/0R3/t+ucqAPRHf/RHf/SPgP77FQD6oz/6oz/6R0P/lgWA/uiP/uiP/pHRv1kBoD/6oz/6o3+U9N9bAOiP/uiP/ugfMf1FxER/9Ed/9Ef/COovRlFjcOiP/uiP/uivTX8pYgwO/dEf/dEf/RXqL35jcOiP/uiP/uivU38pOAaH/uiP/uiP/mr1l/xjcOiP/uiP/uivWf98Y3Doj/7oj/7or1x/yVUA6I/+6I/+6K9f//0LAP3RH/3RH/0joX+rAkB/9Ed/9Ef/qOjfvADQH/3RH/3RP0L6f1MA6I/+6I/+6B8t/ZsKAP3RH/3RH/0jp7+IYYbjyNAf/dEf/dG/XfWXIraA0B/90R/90V+h/uK3BYT+6I/+6I/+OvWXgltA6I/+6I/+6K9Wf8m/BYT+6I/+6I/+mvXPtwWE/uiP/uiP/sr1l2IKAP3RH/3RH/316e9fAOiP/uiP/uivUn+fAkB/9Ed/9Ed/rfoXKgD0R3/0R3/0V6x/3gJAf/RHf/RHf9365y4A9Ed/9Ed/9Fevf44CQH/0R3/0R/8o6N+6ANAf/dEf/dE/IvpL3jE49Ed/9Ed/9Fetv+Qeg0N/9Ed/9Ed/7fpLjjE49Ed/9Ed/9I+A/tJ6DA790R/90R/9o6F/yzE49Ed/9Ed/9I+M/rKvANAf/dEf/dE/SvrvLQD0R3/0R3/0j5j+ImKiP/qjP/qjfwT1F6PIMTj0R3/0R3/016W/FDUGh/7oj/7oj/7q9Bf/MTj0R3/0R3/016i/+IzBoT/6oz/6o79S/aXQGBz6oz/6oz/669Vf8o7BoT/6oz/6o79q/SX3GBz6oz/6oz/6a9dfcozBoT/6oz/6o38E9JfWY3Doj/7oj/7oHw39Dcn/i2Doj/7oj/7or1h/KaYA0B/90R/90V+f/v4FgP7oj/7oj/4q9fcpAPRHf/RHf/TXqn+hAkB/9Ed/9Ed/xfpLOWNw6I/+6I/+6F+9+kvJY3Doj/7oj/7oX9X6S2ljcOiP/uiP/uhf7fpLCWNw6I/+6I/+6K9Af2nrGBz6oz/6oz/669Bf2jQGh/7oj/7oj/5q9Jfix+DQH/3RH/3RX5P+UuQYHPqjP/qjP/or07+oMTj0R3/0R3/016e/+G8BoT/6oz/6o79G/X0KAP3RH/3RH/216l+oANAf/dEf/dFfsf55CwD90R/90R/9deufuwDQH/3RH/3RX73+OQoA/dEf/dEf/aOgf+sCQH/0R3/0R/+I6N+iANAf/dEf/dE/OvrvKwD0R3/0R3/0j5T+ewoA/dEf/dEf/aOmv4iY6I/+6I/+6B9B/Q3D+P+ZUECfi1kskwAAAABJRU5ErkJggg=="  # ikona aplikace (PNG, base64)

# Volitelné cloudové ukládání To-do listu (Upstash Redis, zdarma). Bez těchto proměnných
# se To-do ukládá jen v zařízení.
RURL = os.environ.get("UPSTASH_REDIS_REST_URL", "").rstrip("/")
RTOK = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
SECRET = hashlib.sha256((PIN + "|zakovka").encode()).hexdigest() if PIN else secrets.token_hex(16)

def call(url, data=None, token=None):
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def safe(f):
    try:
        return f()
    except Exception:
        return None

def redis(cmd):
    req = urllib.request.Request(RURL, data=json.dumps(cmd).encode(), method="POST",
                                 headers={"Authorization": "Bearer " + RTOK, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r).get("result")

def sign(uid):
    return hmac.new(SECRET.encode(), uid.encode(), hashlib.sha256).hexdigest()

def save_todo(d):
    uid = str(d.get("uid", ""))
    if not RURL or len(uid) != 32 or not hmac.compare_digest(sign(uid), str(d.get("tok", ""))):
        return 403, json.dumps({"ok": False})
    items = d.get("items")
    if not isinstance(items, list) or len(items) > 500:
        return 400, json.dumps({"ok": False})
    j = json.dumps(items, ensure_ascii=False)
    if len(j) > 200000:
        return 400, json.dumps({"ok": False})
    redis(["SET", "zakovka:todo:" + uid, j])
    return 200, json.dumps({"ok": True})

def fetch_all(base, user, pwd):
    p = urllib.parse.urlparse(base if "://" in base else "https://" + base)
    if p.scheme != "https" or not p.netloc:
        raise ValueError("Adresa školy musí být https://…")
    path = p.path
    for cut in ("/api", "/next", "/login", "/default"):
        if cut in path.lower():
            path = path[:path.lower().index(cut)]
    root = f"https://{p.netloc}{path.rstrip('/')}"
    body = urllib.parse.urlencode({"client_id": "ANDR", "grant_type": "password",
                                   "username": user, "password": pwd}).encode()
    tok = call(root + "/api/login", body)["access_token"]
    today = datetime.date.today().isoformat()
    out = {
        "marks": call(root + "/api/3/marks", token=tok),
        "absence": safe(lambda: call(root + "/api/3/absence/student", token=tok)),
        "timetable": safe(lambda: call(root + f"/api/3/timetable/actual?date={today}", token=tok)),
    }
    # stabilní anonymní ID uživatele (hash školy a jména) – podle něj se ukládá To-do
    uid = hashlib.sha256((root + "|" + user.strip().lower()).encode()).hexdigest()[:32]
    out["uid"], out["tok"], out["sync"], out["todo"] = uid, sign(uid), False, None
    if RURL:
        try:
            v = redis(["GET", "zakovka:todo:" + uid])
            out["todo"] = json.loads(v) if v else None
            out["sync"] = True
        except Exception:
            pass
    return out

def friendly(e):
    if isinstance(e, urllib.error.HTTPError):
        if e.code in (400, 401):
            return f"Škola odmítla přihlášení (HTTP {e.code}). Zkontroluj jméno a heslo, hlavně velká a malá písmena a znaky jako I a l nebo 0 a O."
        if e.code == 403:
            return "Server školy odmítl připojení (HTTP 403). Může blokovat přístup z cizích serverů."
        if e.code == 404:
            return "Adresa školy nevypadá správně (HTTP 404). Zkontroluj ji."
        return f"Server školy vrátil chybu HTTP {e.code}."
    if isinstance(e, (socket.timeout, TimeoutError)):
        return "Server školy neodpověděl včas. Zkus to za chvíli znovu."
    if isinstance(e, urllib.error.URLError):
        return f"Nepodařilo se připojit k serveru školy: {e.reason}"
    return f"Načtení selhalo: {e}"

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, data, ctype="application/json"):
        b = data if isinstance(data, bytes) else data.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def _ok(self):
        if not PIN:
            return True
        try:
            got = base64.b64decode(self.headers.get("Authorization", "")[6:]).decode().split(":", 1)[1]
        except Exception:
            got = ""
        if hmac.compare_digest(got.encode(), PIN.encode()):
            return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Zakovka"')
        self.send_header("Content-Length", "0")
        self.end_headers()
        return False
    def do_GET(self):
        if self.path.split("?")[0] == "/icon.png":   # ikona je veřejná, iPhone si ji stahuje bez hesla
            b = base64.b64decode(ICON)
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
            return
        if self._ok():
            self._send(200, PAGE, "text/html")
    def do_POST(self):
        if not self._ok():
            return
        try:
            n = int(self.headers["Content-Length"])
            if n > 300000:
                raise ValueError("Požadavek je příliš velký")
            d = json.loads(self.rfile.read(n))
            if self.path.split("?")[0] == "/todo":
                code, body = save_todo(d)
                self._send(code, body)
                return
            self._send(200, json.dumps(fetch_all(d["base"], d["user"], d["pass"])))
        except Exception as e:
            self._send(400, json.dumps({"error": friendly(e)}))

PAGE = r'''<!doctype html>
<html lang="cs"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Žákovka">
<link rel="apple-touch-icon" href="/icon.png">
<meta name="theme-color" content="#4B4DED">
<title>Žákovka</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600&display=swap">
<style>
:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);
--bg:#F2F4F9;--sf:#fff;--ink:#16203A;--mu:#6A7389;--ln:#E3E7F0;--ac:#4B4DED;--acs:#E9E9FD;
--g1:#0E8F72;--g2:#4C9F4F;--g3:#B98300;--g4:#D9622B;--g5:#D13B3B}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0F1424;--sf:#181F36;--ink:#EEF1FA;--mu:#98A1BA;--ln:#262E4A;--ac:#8F91FF;--acs:#262A55;--g1:#2CC5A0;--g2:#7BC47E;--g3:#E0B034;--g4:#F08A55;--g5:#F06A6A}}
:root[data-theme="dark"]{--bg:#0F1424;--sf:#181F36;--ink:#EEF1FA;--mu:#98A1BA;--ln:#262E4A;--ac:#8F91FF;--acs:#262A55;--g1:#2CC5A0;--g2:#7BC47E;--g3:#E0B034;--g4:#F08A55;--g5:#F06A6A}
html{scroll-padding-top:env(safe-area-inset-top,0px)}
*{box-sizing:border-box}
body{margin:0 auto;max-width:560px;padding:20px 20px 104px;background:var(--bg);color:var(--ink);font:400 16px/1.45 Figtree,system-ui,sans-serif}
h1,h2,.num{font-family:"Bricolage Grotesque",system-ui,sans-serif;letter-spacing:-.02em;margin:0}
h1{font-size:1.5rem;font-weight:700}h2{font-size:1.15rem;font-weight:700;margin:32px 0 6px}
.mu{color:var(--mu);font-size:.9rem}
.hero{padding:28px 0 8px}.hero .num{font-size:5.5rem;line-height:1;font-weight:700}
.scale{position:relative;height:6px;border-radius:3px;margin:18px 0 8px;background:linear-gradient(90deg,var(--g1),var(--g2),var(--g3),var(--g4),var(--g5))}
.knob{position:absolute;top:50%;width:20px;height:20px;border-radius:50%;background:var(--bg);border:4px solid var(--ink);transform:translate(-50%,-50%)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.two .num{font-size:1.6rem;font-weight:700}
.list>*{padding:14px 0;border-bottom:1px solid var(--ln)}.list>*:last-child{border:0}
.row{display:flex;justify-content:space-between;align-items:center;gap:12px}
.pill{display:inline-block;padding:2px 10px;border-radius:99px;font-size:.85rem;font-weight:600;background:var(--acs);color:var(--ac)}
.badge{min-width:30px;text-align:center;padding:2px 8px;border-radius:8px;font-weight:600;font-size:.9rem}
.track{position:relative;height:30px;margin:12px 4px 0}
.track:before{content:"";position:absolute;left:0;right:0;top:50%;height:2px;background:var(--ln)}
.tk{position:absolute;bottom:-14px;transform:translateX(-50%);font-size:.7rem;color:var(--mu)}
.dot{position:absolute;top:50%;transform:translate(-50%,-50%);border-radius:4px}
.dot.hyp{opacity:.55;outline:2px dashed var(--ink);outline-offset:1px}
.avgm{position:absolute;top:50%;width:18px;height:18px;border-radius:50%;border:3px solid;background:var(--bg);transform:translate(-50%,-50%)}
button,select{font:inherit;color:var(--ink);background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:7px 12px}
button{cursor:pointer}button.pri{background:var(--ac);border-color:var(--ac);color:#fff;font-weight:600}
.bare{background:none;border:0;padding:0;text-align:left;width:100%;border-radius:0}
.ctl{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px;font-size:.9rem}.ctl select{padding:4px 8px}
.bar{height:6px;border-radius:3px;background:var(--ln);overflow:hidden;margin-top:8px}.bar i{display:block;height:100%;border-radius:3px}
.ok{color:var(--g1)}.wn{color:var(--g3)}.er{color:var(--g5)}
.chk{width:24px;height:24px;border-radius:50%;border:2px solid var(--ln);padding:0;flex:none;display:grid;place-items:center}
.chk.on{background:var(--ac);border-color:var(--ac);color:#fff}
nav{position:fixed;left:0;right:0;bottom:0;background:var(--sf);border-top:1px solid var(--ln);display:flex;justify-content:center;padding:6px 8px calc(6px + env(safe-area-inset-bottom,0px))}
nav button{flex:1;max-width:110px;border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:.72rem;color:var(--mu);padding:6px 0}
nav button.on{color:var(--ac);font-weight:600}nav svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.open{animation:op .2s ease}@keyframes op{from{opacity:0;transform:translateY(-4px)}}
@media(prefers-reduced-motion:reduce){.open{animation:none}}
input{font:inherit;color:var(--ink);background:var(--sf);border:1px solid var(--ln);border-radius:10px;padding:12px;width:100%;margin-bottom:10px}
nav:empty{display:none}
.list{background:var(--sf);border:1px solid var(--ln);border-radius:16px;padding:0 16px;overflow:hidden}
#top{margin-bottom:4px}#top:empty{display:none}.brand{font:700 1.15rem "Bricolage Grotesque",system-ui,sans-serif;letter-spacing:-.02em}
.days{display:flex;gap:8px;margin:14px 0}
.day{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;padding:8px 0;border-radius:14px;font-size:.8rem;color:var(--mu)}
.day b{font-size:1.1rem;color:var(--ink)}.day.on{background:var(--ac);border-color:var(--ac);color:#fff}.day.on b{color:#fff}
.lesson{display:flex;align-items:center;gap:14px}.lt{width:46px;display:flex;flex-direction:column;align-items:center;font-size:.75rem;color:var(--mu)}
.lt b{font:700 1.3rem "Bricolage Grotesque",system-ui,sans-serif;color:var(--ink)}
.lesson.now{background:var(--acs);margin:0 -16px;padding:14px 16px}.ls{font-weight:600}.lesson.cx .ls{text-decoration:line-through;color:var(--mu)}
.pill.bad{background:color-mix(in srgb,var(--g5) 15%,transparent);color:var(--g5)}
.enter>*{animation:up .4s cubic-bezier(.2,.7,.2,1) both}.enter>*:nth-child(2){animation-delay:.05s}.enter>*:nth-child(3){animation-delay:.1s}.enter>*:nth-child(n+4){animation-delay:.15s}
@keyframes up{from{opacity:0;transform:translateY(10px)}}
button{transition:transform .12s,opacity .12s}button:active{transform:scale(.97)}.bare:active{opacity:.6}
@media(prefers-reduced-motion:reduce){.enter>*{animation:none}button{transition:none}}
#login{position:relative;padding-top:6vh}
#login:before{content:"";position:absolute;left:-20px;right:-20px;top:-40px;height:300px;z-index:-1;background:radial-gradient(60% 90% at 50% 0,color-mix(in srgb,var(--ac) 25%,transparent),transparent)}
.logo{width:64px;height:64px;border-radius:20px;display:grid;place-items:center;color:#fff;font:700 2rem "Bricolage Grotesque",system-ui,sans-serif;background:linear-gradient(135deg,var(--ac),#9b6bff);box-shadow:0 10px 30px color-mix(in srgb,var(--ac) 35%,transparent)}
.ltitle{font-size:2.4rem;margin:20px 0 6px}.lsub{color:var(--mu);margin:0 0 28px}
.field{margin-bottom:14px}.field label{display:block;font-size:.8rem;font-weight:500;color:var(--mu);margin-bottom:6px}.field input{margin:0}
.pw{position:relative}.pw input{padding-right:90px}.pw button{position:absolute;right:6px;top:50%;transform:translateY(-50%);border:0;background:none;color:var(--ac);padding:8px}.pw button:active{transform:translateY(-50%)}
#go{width:100%;padding:14px;margin-top:6px;font-size:1.05rem}#go:disabled{opacity:.7}
.lnk{width:100%;border:0;background:none;color:var(--ac);margin-top:8px;padding:12px}
#msg{margin-top:10px;min-height:1.4em}.lock{margin-top:18px;font-size:.8rem;color:var(--mu);text-align:center}
.tag{font-size:.75rem;font-weight:600;padding:2px 8px;border-radius:99px}
.tag.test,.pill.bad{background:color-mix(in srgb,var(--g5) 15%,transparent);color:var(--g5)}
.tag.ukol{background:var(--acs);color:var(--ac)}.tag.akce{background:color-mix(in srgb,var(--g3) 18%,transparent);color:var(--g3)}
.pill.ok{background:color-mix(in srgb,var(--g1) 15%,transparent);color:var(--g1)}

:root{--glow:var(--ac);--sh:0 1px 2px rgba(22,32,58,.04),0 10px 28px rgba(22,32,58,.07)}
@media(prefers-color-scheme:dark){:root:not([data-theme="light"]){--sh:0 10px 28px rgba(0,0,0,.35)}}
:root[data-theme="dark"]{--sh:0 10px 28px rgba(0,0,0,.35)}
html{background:var(--bg)}
body{padding-bottom:124px;font-variant-numeric:tabular-nums}
body:before{content:"";position:fixed;inset:0 0 auto;height:340px;z-index:-1;pointer-events:none;transition:background .6s;background:radial-gradient(70% 100% at 50% 0,color-mix(in srgb,var(--glow) 16%,transparent),transparent)}
h2{font-size:1.05rem;margin:30px 2px 10px}
.list{border-radius:20px;box-shadow:var(--sh);border-color:color-mix(in srgb,var(--ln) 70%,transparent)}
.brand{display:flex;align-items:center;gap:8px}
.brand:before{content:"Ž";width:26px;height:26px;border-radius:8px;display:grid;place-items:center;font-size:.9rem;color:#fff;background:linear-gradient(135deg,var(--ac),#9b6bff)}
.hero{margin-top:10px;padding:26px 22px 20px;border-radius:28px;border:1px solid var(--ln);box-shadow:var(--sh);background:linear-gradient(160deg,color-mix(in srgb,var(--glow) 14%,var(--sf)),var(--sf) 70%)}
.hero .num{font-size:6rem;letter-spacing:-.04em}
.scl{display:flex;justify-content:space-between;font-size:.7rem;color:var(--mu);margin:0 3px}
.hmsg{font-weight:600;margin-top:12px}
.scale{height:8px;border-radius:4px}
.knob{box-shadow:0 2px 8px rgba(0,0,0,.25)}
.track:before{height:3px;border-radius:2px;background:linear-gradient(90deg,color-mix(in srgb,var(--g1) 35%,var(--ln)),var(--ln) 50%,color-mix(in srgb,var(--g5) 35%,var(--ln)))}
.dot{box-shadow:0 1px 3px rgba(0,0,0,.25)}.avgm{box-shadow:0 1px 4px rgba(0,0,0,.2)}
.chev{color:var(--mu);display:grid;transition:transform .25s}.chev.up{transform:rotate(180deg)}
.bar{height:8px;border-radius:4px}.bar i{border-radius:4px}
.abrow{display:flex;gap:18px;align-items:center}
.enter .bar i{animation:grow .9s cubic-bezier(.2,.7,.2,1)}@keyframes grow{from{width:0}}
.enter .arc{animation:arc 1s cubic-bezier(.2,.7,.2,1)}@keyframes arc{from{stroke-dashoffset:214}}
nav{left:14px;right:14px;bottom:calc(10px + env(safe-area-inset-bottom,0px));max-width:532px;margin:0 auto;padding:6px;border-radius:26px;border:1px solid var(--ln);background:color-mix(in srgb,var(--sf) 80%,transparent);-webkit-backdrop-filter:blur(18px) saturate(1.5);backdrop-filter:blur(18px) saturate(1.5);box-shadow:0 12px 32px rgba(22,32,58,.16)}
nav button{border-radius:20px;padding:8px 0;transition:background .2s,color .2s}nav button.on{background:var(--acs)}
button.pri{box-shadow:0 6px 18px color-mix(in srgb,var(--ac) 35%,transparent)}
input:focus,select:focus{outline:2px solid color-mix(in srgb,var(--ac) 55%,transparent);outline-offset:1px;border-color:var(--ac)}
#login>*{animation:up .55s cubic-bezier(.2,.7,.2,1) both}#login>*:nth-child(2){animation-delay:.05s}#login>*:nth-child(3){animation-delay:.1s}#login>*:nth-child(4){animation-delay:.15s}#login>*:nth-child(n+5){animation-delay:.2s}
#go:disabled:after{content:"";display:inline-block;width:14px;height:14px;margin-left:10px;border:2px solid rgba(255,255,255,.4);border-top-color:#fff;border-radius:50%;animation:spin .7s linear infinite;vertical-align:-2px}@keyframes spin{to{transform:rotate(360deg)}}
@media(prefers-reduced-motion:reduce){.enter .bar i,.enter .arc,#login>*,#go:disabled:after{animation:none}body:before{transition:none}}
.form{background:var(--sf);border:1px solid var(--ln);border-radius:20px;padding:16px;box-shadow:var(--sh);margin:12px 0}
.form input,.form select{width:100%;margin:0 0 10px;padding:12px;border-radius:10px}.form label{display:block;margin:2px 0 4px}
.tag.projekt{background:color-mix(in srgb,var(--g1) 15%,transparent);color:var(--g1)}
.dng{color:var(--g5);border-color:color-mix(in srgb,var(--g5) 40%,var(--ln))}
@media print{nav,.noprint{display:none!important}}
</style></head><body>
<div id="login">
<div class="logo">Ž</div>
<h1 class="ltitle">Žákovka</h1>
<p class="lsub">Známky, absence a rozvrh z Bakalářů na jednom místě.</p>
<div class="field"><label for="base">Adresa školy</label><input id="base" placeholder="https://is.skola.cz/IS" inputmode="url" autocapitalize="off" autocorrect="off"></div>
<div class="field"><label for="user">Uživatelské jméno</label><input id="user" autocapitalize="off" autocorrect="off" autocomplete="username"></div>
<div class="field"><label for="pass">Heslo</label><div class="pw"><input id="pass" type="password" autocomplete="current-password"><button id="eye" type="button">Zobrazit</button></div></div>
<button id="go" class="pri">Zobrazit přehled</button>
<button id="demo" class="lnk">Vyzkoušet s ukázkovými daty</button>
<div id="msg" class="mu" role="status"></div>
<div class="lock">Údaje se posílají jen na server tvé školy a nikam se neukládají.</div>
</div>
<header id="top" class="noprint"></header><div id="out"></div><nav id="nav" class="noprint"></nav>
<script>
const val=t=>{const m=String(t||"").trim().match(/^([1-5])(-)?$/);return m?+m[1]+(m[2]?.5:0):null};
const fmt=v=>v%1?(v+.5)+"-":""+v;
const n2=v=>v.toFixed(2).replace(".",",");
const gc=v=>`var(--g${Math.min(5,Math.max(1,Math.round(v+.01)))})`;
function h(tag,props,...kids){const e=document.createElement(tag);Object.assign(e,props||{});kids.flat().forEach(k=>e.append(k));return e}
function sel(opts,v,fn){const e=h("select",{onchange:ev=>fn(ev.target.value)});
 opts.forEach(o=>{const[a,b]=Array.isArray(o)?o:[o,o];const op=h("option",{value:a},String(b));if(String(a)===String(v))op.selected=true;e.append(op)});return e}
const M=(id,t,w,c,d,n)=>({id,t,w,c,d,n});
function dayStr(n){const d=new Date();d.setDate(d.getDate()+n);return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function demoDays(){return[
 {date:dayStr(-2),ok:6,miss:0,late:0,soon:0,sch:0,un:false},{date:dayStr(-9),ok:2,miss:2,late:0,soon:0,sch:0,un:true},
 {date:dayStr(-20),ok:0,miss:0,late:1,soon:0,sch:0,un:false},{date:dayStr(-33),ok:5,miss:0,late:0,soon:1,sch:0,un:false}]}
function demoWeek(){const p=n=>String(n).padStart(2,"0");
 const N=[["Matematika","B12"],["Český jazyk","A5"],["Angličtina","J3"],["Fyzika","F1"],["Dějepis","A8"],["Programování","PC2"],["Tělesná výchova","Tělocvična"]];
 const T=[["7:55","8:40"],["8:50","9:35"],["9:55","10:40"],["10:50","11:35"],["11:45","12:30"],["12:40","13:25"]];
 const mon=new Date();mon.setDate(mon.getDate()-((mon.getDay()+6)%7));
 return[0,1,2,3,4].map(i=>{const d=new Date(mon);d.setDate(mon.getDate()+i);
  return{date:`${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}`,items:T.slice(0,5+(i%2)).map((t,k)=>{const n=N[(i*2+k)%N.length];
   return{h:String(k+1),from:t[0],to:t[1],s:n[0],r:n[1],c:i==2&&k==1?"Suplování":i==2&&k==4?"Odpadá":"",x:i==2&&k==4}})}})}
const DEMO={thr:30,un:1,days:demoDays(),tot:{ok:20,miss:8,late:3,soon:1,sch:0},
 subs:[
  {name:"Matematika",prev:[1.8,1.6],marks:[M(1,"1",3,"Písemka","2026-09-20"),M(2,"2-",5,"Test","2026-10-10"),M(3,"1",2,"Ústní","2026-11-02"),M(4,"2",3,"Domácí úkol","2026-11-12",1)]},
  {name:"Český jazyk",prev:[2.4,2.8],marks:[M(5,"3",4,"Diktát","2026-09-25"),M(6,"2",3,"Slohová práce","2026-10-18"),M(7,"4-",5,"Test","2026-11-05"),M(8,"3",2,"Čtenářský deník","2026-11-13",1)]},
  {name:"Angličtina",prev:[1.4,1.3],marks:[M(9,"1",2,"Slovíčka","2026-09-30"),M(10,"1-",3,"Test","2026-10-22")]},
  {name:"Fyzika",prev:[2.2,2.5],marks:[M(11,"2",3,"Referát","2026-10-01"),M(12,"3-",4,"Test","2026-11-08")]},
  {name:"Dějepis",prev:[2.0,2.2],marks:[M(13,"2",3,"Ústní","2026-09-28"),M(14,"2-",4,"Test","2026-10-25"),M(15,"1",2,"Aktivita","2026-11-10")]}],
 abs:[{n:"Matematika",l:60,b:4},{n:"Český jazyk",l:50,b:9},{n:"Angličtina",l:45,b:2},{n:"Fyzika",l:30,b:10},{n:"Dějepis",l:28,b:3}],
 tt:demoWeek()};
let DATA=DEMO;
const S={tab:"over",open:null,goal:{},hypo:{},w:{},hm:{},hw:{},seen:new Set(),theme:0};
try{S.seen=new Set(JSON.parse(localStorage.getItem("seen")||"[]"))}catch(e){}
const isNew=m=>m.n&&!S.seen.has(m.id),all=s=>s.marks.concat(S.hypo[s.name]||[]);
function avg(ms){let s=0,w=0;ms.forEach(m=>{const v=val(m.t);if(v==null)return;s+=v;w+=1});return w?s/w:null}
function trend(s){const ms=s.marks.slice().sort((a,b)=>a.d.localeCompare(b.d));return ms.map((_,i)=>avg(ms.slice(0,i+1)))}
function spark(p){if(p.length<2)return"";const x=i=>4+i*112/(p.length-1),y=v=>4+(v-1)/4*22;
 const s=document.createElementNS("http://www.w3.org/2000/svg","svg");s.setAttribute("viewBox","0 0 120 30");s.setAttribute("width","120");
 s.innerHTML=`<polyline fill="none" stroke="${gc(p[p.length-1])}" stroke-width="2.5" stroke-linecap="round" points="${p.map((v,i)=>x(i)+","+y(v)).join(" ")}"/>`;return s}
function goalText(s,t){let sm=0,W=0;all(s).forEach(m=>{const v=val(m.t);if(v!=null){sm+=v;W+=1}});
 const x=((t+.5)*(W+1)-sm);
 if(x>=5)return["ok","Cíl už máš splněný, stačí i pětka."];
 if(x<1)return["er","Ani s jedničkou z další písemky cíl nedoženeš."];
 return["wn",`Z další známky potřebuješ aspoň ${fmt(Math.floor(x*2)/2)}.`]}
const mo=()=>[1,1.5,2,2.5,3,3.5,4,4.5,5].map(v=>[v,fmt(v)]);
function badge(t){const v=val(t);return h("span",{className:"badge",style:`color:${gc(v)};background:color-mix(in srgb,${gc(v)} 15%,transparent)`},t)}
function subject(s){
 const a=avg(all(s)),op=S.open===s.name,hy=S.hypo[s.name]||[];
 const tr=h("div",{className:"track"},...[1,2,3,4,5].map(i=>h("span",{className:"tk",style:`left:${(i-1)*25}%`},i)));
 all(s).forEach(m=>{const v=val(m.t);if(v!=null){const z=12;tr.append(h("i",{className:"dot"+(m.c=="Fiktivní"?" hyp":""),style:`left:${(v-1)/4*100}%;width:${z}px;height:${z}px;background:${gc(v)}`}))}});
 tr.append(h("b",{className:"avgm",style:`left:${(a-1)/4*100}%;border-color:${gc(a)}`}));
 const head=h("button",{className:"bare",onclick(){S.open=op?null:s.name;draw()}},
  h("div",{className:"row"},h("span",{style:"font-weight:600"},s.name),
   h("span",{style:"display:flex;align-items:center;gap:8px"},h("span",{className:"num",style:`font-size:1.5rem;font-weight:700;color:${gc(a)}`},n2(a)),chev(op))),tr,h("div",{style:"height:16px"}));
 const box=h("div",{},head);
 if(op){const g=S.goal[s.name]||2,hm=S.hm[s.name]||2,[c,t]=goalText(s,+g),base=avg(s.marks);
  box.append(h("div",{className:"open"},
   h("div",{className:"row"},h("span",{className:"mu"},"Vývoj průměru"),spark(trend(s))),
   h("div",{style:"margin-top:8px"},...s.marks.slice().sort((x,y)=>y.d.localeCompare(x.d)).map(m=>h("div",{className:"row mu",style:"padding:3px 0"},
    h("span",{style:"display:flex;gap:12px"},h("span",{style:"width:52px"},m.d?new Date(m.d+"T12:00:00").toLocaleDateString("cs-CZ",{day:"numeric",month:"numeric"}):""),h("span",{},m.c)),badge(m.t)))),
   hy.length?h("div",{className:"mu",style:"margin-top:6px"},`S fiktivními známkami: ${n2(base)} → ${n2(a)}`):"",
   h("div",{className:"ctl"},"Co když dostanu",sel(mo(),hm,v=>{S.hm[s.name]=+v}),
    h("button",{onclick(){(S.hypo[s.name]=S.hypo[s.name]||[]).push({t:fmt(+hm),w:1,d:"",c:"Fiktivní"});draw()}},"Přidat"),
    hy.length?h("button",{onclick(){S.hypo[s.name]=[];draw()}},"Zrušit"):""),
   h("div",{className:"ctl"},"Chci na vysvědčení",sel([1,2,3,4],g,v=>{S.goal[s.name]=+v;draw()})),
   h("div",{className:c,style:"margin-top:8px;font-weight:500"},t)))}
 return box}
function hmsg(t){return t<=1.3?"Výborné výsledky, skoro samé jedničky.":t<=1.8?"Skvělé výsledky.":t<=2.5?"Dobré výsledky.":t<=3.2?"Je kam se zlepšovat.":"Chce to přidat."}
function countUp(el,to){if(!el||matchMedia("(prefers-reduced-motion:reduce)").matches)return;const t0=performance.now();
 (function f(t){const k=Math.min(1,(t-t0)/700),e=1-Math.pow(1-k,3);el.textContent=n2(1+(to-1)*e);if(k<1)requestAnimationFrame(f)})(t0)}
function ring(f,c){const R=34,C=2*Math.PI*R,s=document.createElementNS("http://www.w3.org/2000/svg","svg");s.setAttribute("viewBox","0 0 84 84");s.setAttribute("width","84");s.setAttribute("height","84");
 s.innerHTML=`<circle cx="42" cy="42" r="${R}" fill="none" stroke="var(--ln)" stroke-width="9"/><circle class="arc" cx="42" cy="42" r="${R}" fill="none" stroke="${c}" stroke-width="9" stroke-linecap="round" stroke-dasharray="${C}" stroke-dashoffset="${C*(1-Math.min(1,f))}" transform="rotate(-90 42 42)"/>`;return s}
function chev(o){const e=h("span",{className:"chev"+(o?" up":"")});e.innerHTML='<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>';return e}
const jed=n=>n==1?"jednička":n<5?"jedničky":"jedniček";
function plan(){const A=DATA.subs.map(s=>{const m=all(s).map(x=>val(x.t)).filter(v=>v!=null);return{n:s.name,sum:m.reduce((a,b)=>a+b,0),c:m.length,k:0}}).filter(x=>x.c);
 const av=x=>(x.sum+x.k)/(x.c+x.k),mean=()=>A.reduce((a,x)=>a+av(x),0)/A.length;
 A.forEach(x=>{if(av(x)>2.5)x.k=Math.ceil((x.sum-2.5*x.c)/1.5)});
 let g=0;while(mean()>1.5&&g<300){let b=null,bd=0;A.forEach(x=>{const d=av(x)-(x.sum+x.k+1)/(x.c+x.k+1);if(d>bd){bd=d;b=x}});if(!b)break;b.k++;g++}
 return{A:A.filter(x=>x.k>0).sort((a,b)=>b.k-a.k),total:A.reduce((a,x)=>a+x.k,0),ok:mean()<=1.5}}
function trendAll(){const ms=DATA.subs.flatMap(s=>s.marks.map(m=>({s:s.name,v:val(m.t),d:m.d}))).filter(m=>m.v!=null&&m.d).sort((a,b)=>a.d.localeCompare(b.d));
 const sub={},P=[];ms.forEach((m,i)=>{(sub[m.s]=sub[m.s]||[]).push(m.v);
  if(i==ms.length-1||ms[i+1].d!=m.d){const k=Object.values(sub);P.push({d:m.d,a:k.reduce((x,l)=>x+l.reduce((p,q)=>p+q,0)/l.length,0)/k.length})}});return P}
function chart(P){const W=320,H=150,l=28,r=12,t=14,b=22,T=d=>new Date(d+"T12:00:00").getTime(),d0=T(P[0].d),d1=T(P[P.length-1].d);
 const hi=Math.max(3,Math.ceil(Math.max(...P.map(p=>p.a))+.1)),X=d=>l+(T(d)-d0)/((d1-d0)||1)*(W-l-r),Y=v=>t+(v-1)/(hi-1)*(H-t-b),last=P[P.length-1];
 const pts=P.map(p=>X(p.d)+","+Y(p.a)).join(" "),f=d=>new Date(d+"T12:00:00").toLocaleDateString("cs-CZ",{day:"numeric",month:"numeric"});
 let g="";for(let v=1;v<=hi;v++)g+=`<line x1="${l}" x2="${W-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--ln)"/><text x="${l-8}" y="${Y(v)+4}" text-anchor="end" font-size="10" fill="var(--mu)">${v}</text>`;
 const s=document.createElementNS("http://www.w3.org/2000/svg","svg");s.setAttribute("viewBox",`0 0 ${W} ${H}`);s.setAttribute("width","100%");
 s.innerHTML=`<defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--ac);stop-opacity:.28"/><stop offset="1" style="stop-color:var(--ac);stop-opacity:0"/></linearGradient></defs>${g}
 <polygon fill="url(#ga)" points="${X(P[0].d)},${H-b} ${pts} ${X(last.d)},${H-b}"/><polyline fill="none" stroke="var(--ac)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round" points="${pts}"/>
 ${P.map(p=>`<circle cx="${X(p.d)}" cy="${Y(p.a)}" r="3" fill="var(--sf)" stroke="var(--ac)" stroke-width="2"/>`).join("")}
 <text x="${l}" y="${H-4}" font-size="10" fill="var(--mu)">${f(P[0].d)}</text><text x="${W-r}" y="${H-4}" text-anchor="end" font-size="10" fill="var(--mu)">${f(last.d)}</text>
 <text x="${Math.min(X(last.d),W-r-14)}" y="${Y(last.a)-10}" text-anchor="middle" font-size="11" font-weight="700" fill="var(--ink)">${n2(last.a)}</text>`;return s}
function overview(o){
 const L=DATA.subs.map(s=>({s,a:avg(all(s))})),tot=L.reduce((x,y)=>x+y.a,0)/L.length,so=[...L].sort((x,y)=>x.a-y.a),
  b=Math.max(DATA.abs.reduce((x,y)=>x+y.b,0),DATA.tot?DATA.tot.ok+DATA.tot.miss:0),l=DATA.abs.reduce((x,y)=>x+y.l,0),p=l?b/l*100:0;
 o.append(h("div",{className:"hero"},h("div",{className:"mu"},"Celkový průměr"),h("div",{className:"num",id:"avgnum",style:"color:"+gc(tot)},n2(tot)),
  h("div",{className:"scale"},h("i",{className:"knob",style:`left:${(tot-1)/4*100}%`})),
  h("div",{className:"scl"},...[1,2,3,4,5].map(i=>h("span",{},String(i)))),h("div",{className:"hmsg"},hmsg(tot))));
 document.documentElement.style.setProperty("--glow",gc(tot));if(o.className=="enter")countUp(document.getElementById("avgnum"),tot);
 const rowOf=x=>h("div",{className:"row"},h("span",{style:"font-weight:600"},x.s.name),h("span",{className:"num",style:`font-weight:700;color:${gc(x.a)}`},n2(x.a)));
 const tie=v=>so.filter(x=>n2(x.a)==n2(v));
 o.append(h("h2",{},"Nejlépe ti jde"),h("div",{className:"list"},...tie(so[0].a).map(rowOf)));
 o.append(h("h2",{},"Nejvíc se vyplatí zabrat"),h("div",{className:"list"},...tie(so[so.length-1].a).map(rowOf)));
 const tp=trendAll();
 if(tp.length>1)o.append(h("h2",{},"Vývoj průměru"),h("div",{className:"list"},h("div",{style:"padding:12px 6px 6px"},chart(tp),h("div",{className:"mu",style:"margin-top:4px"},"Čím výš, tím lepší průměr."))));
 const bad=L.filter(x=>x.a>2.5),c1=tot<=1.5,okH=c1&&!bad.length,pl=okH?null:plan();
 o.append(h("h2",{},"Vyznamenání"),h("div",{className:"list"},
  h("div",{className:"row"},h("b",{className:okH?"ok":"er"},okH?"Podmínky zatím splňuješ":"Podmínky zatím nesplňuješ")),
  h("div",{className:"row"},h("span",{},"Celkový průměr do 1,50"),h("span",{className:c1?"ok":"er"},(c1?"✓ ":"✕ ")+n2(tot))),
  h("div",{className:"row"},h("span",{},"Průměr každého předmětu do 2,50"),h("span",{className:bad.length?"er":"ok",style:"text-align:right"},bad.length?"✕ "+bad.map(x=>x.s.name).join(", "):"✓")),
  pl?h("div",{className:"row"},h("span",{},"K vyznamenání chybí"),h("b",{className:"er",style:"text-align:right"},pl.ok?`zhruba ${pl.total} ${jed(pl.total)}`:"příliš mnoho jedniček")):"",
  pl&&pl.ok&&pl.A.length?h("div",{className:"mu"},"Nejvíc pomůžou: "+pl.A.slice(0,3).map(x=>x.n+" (+"+x.k+")").join(", ")):"",
  h("div",{className:"mu"},"Orientační údaj. Pravidla školy a hodnocení chování se mohou lišit.")));
 const est=a=>a<=1.5?1:a<=2.5?2:a<=3.5?3:a<=4.5?4:5;
 o.append(h("h2",{},"Odhad vysvědčení"),h("div",{className:"list"},...so.map(x=>{const g=est(x.a),near=g<5&&x.a>g+.5-.15,note=g==5?"Hrozí nedostatečná":g==4?"Pozor, čtyřka":near?"Blízko horší známce":"";
  return h("div",{className:"row"},h("span",{},h("div",{style:"font-weight:600"},x.s.name),note?h("div",{className:g>=4?"er":"wn",style:"font-size:.85rem"},note):""),
   h("span",{className:"badge",style:`font-size:1.05rem;color:${gc(g)};background:color-mix(in srgb,${gc(g)} 15%,transparent)`},String(g)))})),
  h("div",{className:"mu",style:"margin:8px 2px 0"},"Odhad podle průměrů. Učitel může známku určit jinak."));
 o.append(h("h2",{},"Absence"),h("div",{className:"list"},h("div",{className:"abrow"},
  ring(l?p/DATA.thr:0,p>=DATA.thr?"var(--g5)":p>=DATA.thr*.6?"var(--g3)":"var(--g1)"),
  h("div",{},h("div",{className:"num",style:"font-size:2rem;font-weight:700"},l?n2(p).replace(/,?0$/,"")+" %":b+" h"),
   h("div",{className:"mu"},`${b}${l?" z "+l:""} hodin${l?", limit "+DATA.thr+" %":""}`),
   DATA.tot?h("div",{className:"mu",style:"margin-top:4px"},`Omluveno ${DATA.tot.ok} h, neomluveno ${DATA.tot.miss} h, pozdní příchody ${DATA.tot.late}`):""))));
 if(DATA.subs.every(s=>s.prev))o.append(h("h2",{},"Oproti loňsku"),h("div",{className:"list"},...L.map(({s,a})=>{const d=a-s.prev[1];
  return h("div",{className:"row"},h("span",{},s.name),h("span",{className:d<-.05?"ok":d>.05?"er":"mu"},d<-.05?"lepší o "+n2(-d):d>.05?"horší o "+n2(d):"stejné"))})))}
function daysBlock(o){const D=DATA.days||[];if(!D.length)return;
 o.append(h("h2",{},"Dny s absencí"),h("div",{className:"list"},...D.map(d=>{
  const parts=[d.ok&&`omluveno ${d.ok} h`,d.miss&&`neomluveno ${d.miss} h`,d.late&&`pozdní příchod ${d.late} h`,d.soon&&`předčasný odchod ${d.soon} h`,d.sch&&`škola ${d.sch} h`].filter(Boolean);
  return h("div",{className:"row"},h("span",{},h("div",{style:"font-weight:600"},new Date(d.date+"T12:00:00").toLocaleDateString("cs-CZ",{weekday:"long",day:"numeric",month:"long"})),h("div",{className:"mu"},parts.join(", ")||"bez zameškaných hodin")),
   d.un||d.miss?h("span",{className:"pill bad"},d.un?"k omluvení":"neomluveno"):h("span",{className:"pill ok"},"omluveno"))})))}
function absence(o){
 o.append(h("h1",{},"Absence"),h("div",{className:"mu"},`Limit je ${DATA.thr} % zameškaných hodin v předmětu.`),
  DATA.tot?h("div",{className:"list",style:"margin-top:12px"},...[["Omluvené hodiny",DATA.tot.ok],["Neomluvené hodiny",DATA.tot.miss],["Pozdní příchody",DATA.tot.late],["Předčasné odchody",DATA.tot.soon],["Školní akce",DATA.tot.sch]].map(([k,v])=>h("div",{className:"row"},h("span",{},k),h("b",{className:k=="Neomluvené hodiny"&&v?"er":""},String(v))))):"",h("div",{className:"list",style:"margin-top:12px"},
  ...DATA.abs.map(a=>({...a,p:a.l?a.b/a.l*100:0,left:Math.floor(DATA.thr/100*a.l-a.b+1e-9)})).sort((x,y)=>y.p-x.p).map(x=>
   h("div",{},h("div",{className:"row"},h("span",{style:"font-weight:600"},x.n),h("span",{className:x.p>=DATA.thr?"er":""},n2(x.p)+" %")),
    h("div",{className:"bar"},h("i",{style:`width:${Math.min(100,x.p/DATA.thr*100)}%;background:var(--${x.p>=DATA.thr?"g5":x.p>=DATA.thr*.6?"g3":"g1"})`})),
    h("div",{className:"mu",style:"margin-top:6px"},x.left<0?"Limit je překročený.":`Můžeš zameškat ještě ${x.left} ${x.left==1?"hodinu":x.left>=2&&x.left<=4?"hodiny":"hodin"}.`)))));
 daysBlock(o);if(DATA.un)o.append(h("div",{className:"er",style:"margin-top:16px;font-weight:600"},`Máš ${DATA.un} ${DATA.un==1?"neomluvený den":DATA.un<5?"neomluvené dny":"neomluvených dnů"}.`))}
function today(o){
 const days=DATA.tt.filter(d=>{const g=new Date(d.date+"T12:00:00").getDay();return g>=1&&g<=5});
 const n=new Date(),ds=`${n.getFullYear()}-${pad(n.getMonth()+1)}-${pad(n.getDate())}`;
 if(!S.day||!days.some(d=>d.date==S.day))S.day=(days.find(d=>d.date==ds)||days.find(d=>d.date>ds)||days[0]||{}).date;
 o.append(h("h1",{},"Rozvrh"));
 if(!days.length)o.append(h("div",{className:"mu",style:"margin-top:8px"},"Rozvrh se nepodařilo načíst."));
 else{
  o.append(h("div",{className:"days"},...days.map(d=>{const dt=new Date(d.date+"T12:00:00");
   return h("button",{className:"day"+(d.date==S.day?" on":""),onclick(){S.day=d.date;draw()}},h("span",{},dt.toLocaleDateString("cs-CZ",{weekday:"short"}).replace(".","")),h("b",{},String(dt.getDate())))})));
  const d=days.find(x=>x.date==S.day),hm=pad(n.getHours())+":"+pad(n.getMinutes()),tm=t=>(t||"").padStart(5,"0");
  o.append(d.items.length?h("div",{className:"list"},...d.items.map(r=>{const now=d.date==ds&&r.from&&tm(r.from)<=hm&&hm<tm(r.to);
   return h("div",{className:"lesson"+(now?" now":"")+(r.x?" cx":"")},
    h("div",{className:"lt"},h("b",{},r.h),h("span",{},r.from)),
    h("div",{style:"flex:1;min-width:0"},h("div",{className:"ls"},r.s),h("div",{className:"mu"},r.r)),
    r.c?h("span",{className:"pill"+(r.x?" bad":"")},r.c):now?h("span",{className:"pill"},"teď"):"")})):h("div",{className:"mu",style:"margin-top:12px"},"V tento den nejsou žádné hodiny."))}
 }
const KIND={test:"Test",ukol:"Úkol",projekt:"Projekt"};
function stText(){return S.st=="cloud"?"Ukládá se do tvého účtu, uvidíš to i po novém přihlášení.":S.st=="saving"?"Ukládám…":S.st=="err"?"Nepodařilo se uložit do cloudu. Změny jsou zatím jen v tomto zařízení.":"Ukládá se jen v tomto zařízení."}
function todoLoad(d){S.uid=d.uid||"demo";S.tok=d.tok||"";S.sync=!!d.sync;let L=null;
 if(S.sync&&Array.isArray(d.todo))L=d.todo;
 if(!L){try{L=JSON.parse(localStorage.getItem("todo:"+S.uid)||"null")}catch(e){}}
 S.todo=Array.isArray(L)?L:[];S.form=null;S.tf="all";S.busy=false;S.dirty=false;S.st=S.sync?"cloud":"local";
 if(S.sync&&d.todo===null&&S.todo.length)todoSave()}
function todoPush(){S.busy=true;S.st="saving";
 fetch("/todo",{method:"POST",body:JSON.stringify({uid:S.uid,tok:S.tok,items:S.todo})}).then(r=>r.json()).then(r=>{S.st=r.ok?"cloud":"err"}).catch(()=>{S.st="err"})
  .then(()=>{S.busy=false;if(S.dirty){S.dirty=false;todoPush()}else{const e=document.getElementById("tst");if(e)e.textContent=stText()}})}
function todoSave(){try{localStorage.setItem("todo:"+S.uid,JSON.stringify(S.todo))}catch(e){}
 if(!S.sync)return;if(S.busy){S.dirty=true;return}todoPush()}
function newForm(x){return x?Object.assign({},x):{kind:"ukol",title:"",subj:"",date:"",note:""}}
function todoForm(){const f=S.form,
 inp=(ph,k,type)=>h("input",{placeholder:ph,type:type||"text",value:f[k]||"",maxLength:k=="note"?300:120,oninput(ev){f[k]=ev.target.value}}),t=inp("Název, např. Test z matematiky","title");
 return h("div",{className:"form"},
  h("div",{className:"days",style:"margin:0 0 12px"},...Object.entries(KIND).map(([k,n])=>h("button",{className:"day"+(f.kind==k?" on":""),style:"padding:10px 0;font-size:.9rem",onclick(){f.kind=k;draw()}},n))),
  t,sel([["","Předmět (volitelně)"],...DATA.subs.map(s=>[s.name,s.name])],f.subj,v=>{f.subj=v}),
  h("label",{className:"mu"},"Termín (volitelně)"),inp("","date","date"),inp("Téma nebo poznámka (volitelně)","note"),
  h("div",{className:"row"},
   f.id?h("button",{className:"dng",onclick(){if(confirm("Smazat tuto položku?")){S.todo=S.todo.filter(x=>x.id!=f.id);S.form=null;todoSave();draw()}}},"Smazat"):h("span"),
   h("span",{style:"display:flex;gap:8px"},h("button",{onclick(){S.form=null;draw()}},"Zrušit"),
    h("button",{className:"pri",onclick(){if(!f.title.trim()){t.focus();return}
     const it={id:f.id||"t"+Date.now().toString(36)+Math.random().toString(36).slice(2,5),kind:f.kind,title:f.title.trim().slice(0,120),subj:f.subj,date:f.date,note:(f.note||"").trim().slice(0,300),done:!!f.done},i=S.todo.findIndex(x=>x.id==it.id);
     if(i>=0)S.todo[i]=it;else{if(S.todo.length>=300){alert("Je tu příliš mnoho položek, smaž nějaké hotové.");return}S.todo.push(it)}
     S.form=null;todoSave();draw()}},"Uložit"))))}
function todo(o){
 const f=S.tf||"all",today=dayStr(0),dn=n=>n==1?"den":n<5?"dny":"dní",
  dd=x=>x.date?Math.round((new Date(x.date+"T12:00:00")-new Date(today+"T12:00:00"))/864e5):null;
 const grp=x=>{if(x.done)return"Hotovo";const d=dd(x);return d===null?"Bez termínu":d<0?"Po termínu":d==0?"Dnes":d==1?"Zítra":d<=7?"Tento týden":"Později"};
 o.append(h("div",{className:"row"},h("h1",{},"To-do"),h("button",{className:"pri",onclick(){S.form=newForm();draw();scrollTo(0,0)}},"+ Přidat")),
  h("div",{className:"mu",id:"tst",style:"margin-top:4px"},stText()));
 if(S.form)o.append(todoForm());
 o.append(h("div",{className:"days",style:"margin:12px 0"},...[["all","Vše"],["test","Testy"],["ukol","Úkoly"],["projekt","Projekty"]].map(([k,n])=>
  h("button",{className:"day"+(f==k?" on":""),style:"padding:10px 0;font-size:.9rem",onclick(){S.tf=k;draw()}},n))));
 const items=S.todo.filter(x=>f=="all"||x.kind==f).sort((a,b)=>(a.date||"9999").localeCompare(b.date||"9999")||a.title.localeCompare(b.title,"cs"));
 if(!items.length&&!S.form)o.append(h("div",{className:"mu",style:"margin-top:16px"},"Zatím tu nic není. Ťukni na „+ Přidat“ a zapiš si test, úkol nebo projekt."));
 ["Po termínu","Dnes","Zítra","Tento týden","Později","Bez termínu","Hotovo"].forEach(g=>{const L=items.filter(x=>grp(x)==g);if(!L.length)return;
  o.append(h("h2",{},g),h("div",{className:"list"},...L.map(x=>{const d=dd(x);
   return h("div",{className:"row",style:"align-items:flex-start;"+(x.done?"opacity:.5":"")},
    h("button",{className:"bare",style:"flex:1;min-width:0",onclick(){S.form=newForm(x);draw();scrollTo(0,0)}},
     h("div",{},h("span",{className:"tag "+x.kind},KIND[x.kind]||"Úkol"),x.subj?h("b",{style:"margin-left:8px"},x.subj):""),
     h("div",{style:"margin-top:4px;font-weight:500"+(x.done?";text-decoration:line-through":"")},x.title),
     x.note?h("div",{className:"mu"},x.note):""),
    d===null?"":h("span",{style:"text-align:right;white-space:nowrap"},h("div",{style:"font-weight:600"},new Date(x.date+"T12:00:00").toLocaleDateString("cs-CZ",{weekday:"short",day:"numeric",month:"numeric"})),
     h("div",{className:"mu"},d<0?(d==-1?"včera":"před "+(-d)+" dny"):d==0?"dnes":d==1?"zítra":"za "+d+" "+dn(d))),
    h("button",{className:"chk"+(x.done?" on":""),"aria-label":"Hotovo",onclick(){x.done=!x.done;todoSave();draw()}},x.done?"✓":""))})))})}
function more(o){
 const nm=["automatický","světlý","tmavý"];
 o.append(h("h1",{},"Více"),h("div",{className:"list",style:"margin-top:12px"},h("div",{className:"row"},h("span",{},"Účet"),h("button",{onclick(){location.reload()}},"Odhlásit")),
  
  
  
  h("div",{className:"row"},h("span",{},"Vzhled: "+nm[S.theme]),h("button",{onclick(){S.theme=(S.theme+1)%3;const r=document.documentElement;S.theme?r.setAttribute("data-theme",S.theme==1?"light":"dark"):r.removeAttribute("data-theme");draw()}},"Změnit")),
  h("div",{className:"row"},h("span",{},"Uložit přehled jako PDF"),h("button",{onclick(){try{window.print()}catch(e){}}},"Tisk")),
  h("div",{},h("div",{style:"font-weight:500"},"Přidat na plochu iPhonu"),h("div",{className:"mu"},"V Safari ťukni na Sdílet a vyber „Přidat na plochu“."))))}
const IC={over:"M4 11l8-7 8 7v9H4zM10 20v-6h4v6",subj:"M5 6h14M5 12h14M5 18h9",abs:"M7 3v3M17 3v3M4 8h16v12H4zM9 13l6 4M15 13l-6 4",today:"M12 7v5l3 2M12 3a9 9 0 100 18 9 9 0 000-18",more:"M6 12h.01M12 12h.01M18 12h.01",todo:"M5 7l2 2 3-3M5 15l2 2 3-3M13 8h6M13 16h6"};
const TABS=[["over","Přehled"],["subj","Předměty"],["abs","Absence"],["today","Rozvrh"],["todo","To-do"],["more","Více"]];
function draw(){
 const nav=document.getElementById("nav");nav.replaceChildren(...TABS.map(([k,n])=>{const b=h("button",{className:S.tab==k?"on":"",onclick(){S.tab=k;draw();scrollTo(0,0)}});
  b.innerHTML=`<svg viewBox="0 0 24 24"><path d="${IC[k]}"/></svg>`;b.append(n);return b}));
 const top=document.getElementById("top");top.replaceChildren(h("div",{className:"row"},h("span",{className:"brand"},"Žákovka"),h("span",{className:"mu"},new Date().toLocaleDateString("cs-CZ",{weekday:"long",day:"numeric",month:"long"}))));
 const o=document.getElementById("out");o.replaceChildren();o.className=S.last!==S.tab?"enter":"";S.last=S.tab;
 ({over:overview,subj:o=>{o.append(h("h1",{},"Předměty"),h("div",{className:"mu"},"Každá tečka je jedna známka, kroužek je průměr. Ťukni na předmět."),
  h("div",{className:"list",style:"margin-top:12px"},...DATA.subs.slice().sort((a,b)=>avg(all(a))-avg(all(b))).map(subject)))},abs:absence,today,todo,more})[S.tab](o)}
const $=id=>document.getElementById(id);
const pad=n=>String(n).padStart(2,"0");
function convTT(t){
 if(!t||!t.Days)return[];
 const hrs={},sub={},room={};
 (t.Hours||[]).forEach(x=>hrs[x.Id]=x);(t.Subjects||[]).forEach(x=>sub[x.Id]=x.Name);(t.Rooms||[]).forEach(x=>room[x.Id]=x.Abbrev);
 return t.Days.map(d=>({date:(d.Date||"").slice(0,10),
  items:(d.Atoms||[]).slice().sort((a,b)=>a.HourId-b.HourId).map(a=>{const hr=hrs[a.HourId]||{},c=a.Change;
   return{h:hr.Caption||"",from:hr.BeginTime||"",to:hr.EndTime||"",s:sub[a.SubjectId]||(c&&c.Description)||"—",r:room[a.RoomId]||"",
    c:c?(c.TypeName||c.Description||"Změna"):"",x:!!(c&&/cancel|remov|odpad|zruš/i.test((c.ChangeType||"")+(c.TypeName||"")))}})})).filter(d=>d.date)}
function dIso(x){if(!x)return"";const d=new Date(x);return isNaN(d)?String(x).slice(0,10):`${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`}
function convert(r){
 const subs=(r.marks.Subjects||[]).map(s=>({name:s.Subject.Name,prev:null,
  marks:(s.Marks||[]).filter(m=>!m.IsPoints).map(m=>M(m.Id,m.MarkText,1,m.TypeNote||m.Caption||m.Theme||"",(m.MarkDate||"").slice(0,10),m.IsNew?1:0))}))
  .filter(s=>s.marks.some(m=>val(m.t)!=null));
 if(!subs.length)throw new Error("Žádné známky k zobrazení.");
 const ab=r.absence||{};let thr=ab.PercentageThreshold??0.3;if(thr<=1)thr*=100;
 const days=ab.Absences||[],sum=k=>days.reduce((x,d)=>x+(+d[k]||0),0);
 const abs=(ab.AbsencesPerSubject||[]).map(a=>({n:a.SubjectName,l:+a.LessonsCount||0,b:+a.Base||0}));
 return{thr,subs,un:days.filter(a=>a.Unsolved).length,abs,
  tot:{ok:sum("Ok"),miss:sum("Missed"),late:sum("Late"),soon:sum("Soon"),sch:sum("School")},
  
  tt:convTT(r.timetable),uid:r.uid,tok:r.tok,sync:r.sync,todo:r.todo,
  days:days.filter(d=>["Ok","Missed","Late","Soon","School"].some(k=>+d[k]>0)||d.Unsolved).map(d=>({date:dIso(d.Date),ok:+d.Ok||0,miss:+d.Missed||0,late:+d.Late||0,soon:+d.Soon||0,sch:+d.School||0,un:!!d.Unsolved})).sort((a,b)=>b.date.localeCompare(a.date))}}
function start(d){DATA=d;todoLoad(d);S.tab="over";S.open=null;S.hypo={};S.goal={};S.hw={};$("login").style.display="none";draw()}
$("go").onclick=async()=>{
 $("go").disabled=true;$("go").textContent="Přihlašuji…";$("msg").className="mu";$("msg").textContent="První načtení může trvat až minutu.";
 try{const r=await fetch("/",{method:"POST",body:JSON.stringify({base:$("base").value.trim(),user:$("user").value.trim(),pass:$("pass").value})});
  const d=await r.json();if(d.error)throw new Error(d.error);
  $("pass").value="";try{localStorage.setItem("login",JSON.stringify({base:$("base").value.trim(),user:$("user").value.trim()}))}catch(e){}$("msg").textContent="";start(convert(d))}
 catch(e){$("msg").className="er";$("msg").textContent=e.message;$("go").disabled=false;$("go").textContent="Zobrazit přehled"}};
try{const sv=JSON.parse(localStorage.getItem("login")||"{}");$("base").value=sv.base||"";$("user").value=sv.user||""}catch(e){}
$("eye").onclick=()=>{const q=$("pass");q.type=q.type=="password"?"text":"password";$("eye").textContent=q.type=="password"?"Zobrazit":"Skrýt"};
$("demo").onclick=()=>start(DEMO);
</script></body></html>
'''

if __name__ == "__main__":
    local = HOST == "127.0.0.1"
    if not local and not PIN:
        raise SystemExit("Server je dostupný z internetu. Nastav proměnnou prostředí APP_PIN (přístupové heslo).")
    print(f"Běží na http://127.0.0.1:{PORT}  (Ctrl+C ukončí)" if local else f"Běží na portu {PORT}")
    if local:
        webbrowser.open(f"http://127.0.0.1:{PORT}")
    HTTPServer((HOST, PORT), H).serve_forever()
