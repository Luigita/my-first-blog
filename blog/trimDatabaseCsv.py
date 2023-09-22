# importing the pandas library
import base64
import os.path
import zipfile

import PySimpleGUI as Sg
import pandas as pd

from django.shortcuts import render
from .models import Post
from django.utils import timezone


def convert_database(request):
	layout = [[
		Sg.Button('Converti'),
		Sg.Input(key="-IN2-", readonly=True),
		Sg.FileBrowse("Seleziona file", key="-IN-", file_types=("File ZIP", ".zip")),
		Sg.Button("Termina")
	]]

	window = Sg.Window('Window Title', layout, size=(600, 60), resizable=True)

	while True:

		try:
			esiste_persiane = False
			esiste_tapparelle = False

			event, values = window.read()
			print(values["-IN2-"])

			# See if user wants to quit or window was closed
			if event == Sg.WINDOW_CLOSED or event == "Termina":
				window.close()
				break
			elif event == "Converti":
				a = 0

				zip_file = values["-IN-"]

				zip_dir = os.path.dirname(zip_file)

				zip_name = os.path.splitext(os.path.basename(zip_file))[0]

				with zipfile.ZipFile(zip_file, 'r') as zip_ref:
					zip_ref.extractall(
						zip_dir + "/" + zip_name
					)

				unzippedFolder = zip_dir + "/" + zip_name

				if not os.path.exists(unzippedFolder):
					os.makedirs(unzippedFolder)

				# reading the csv file

				if os.path.exists(unzippedFolder + "/persiane.csv"):
					df1 = pd.read_csv(unzippedFolder + "/persiane.csv", sep=";")
					esiste_persiane = True

				if os.path.exists(unzippedFolder + "/tapparelle.csv"):
					df2 = pd.read_csv(unzippedFolder + "/tapparelle.csv", sep=";")
					esiste_tapparelle = True

				if esiste_persiane:
					if os.path.exists(unzippedFolder + "/configurazionePersiane.csv"):
						df = pd.read_csv(unzippedFolder + "/configurazionePersiane.csv", sep=";")
						while a != len(df.index):
							encodedImage = df.loc[a, "blob"]
							if encodedImage == encodedImage:
								decodedImage = base64.b64decode(encodedImage)
								if not os.path.exists(unzippedFolder + "/Foto persiane"):
									os.makedirs(unzippedFolder + "/Foto persiane")
									# imageName = unzippedFolder + "/Foto persiane/" + df["riferimento"].values[a] + {} +
									# ".jpg".format(a)
									imageName = f"{unzippedFolder}/Foto persiane/{df['riferimento'].values[a]}{a}.jpg"
								else:
									# imageName = unzippedFolder + "/Foto persiane/" + df["riferimento"].values[a] + {} +
									# ".jpg".format(a)
									imageName = f"{unzippedFolder}/Foto persiane/{df['riferimento'].values[a]}{a}.jpg"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "blob"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Foto persiane/{df['riferimento'].values[a]}{a}.jpg\"; \"{df['riferimento'].values[a]}{a}.jpg\")"
								imgFile = open(imageName, "wb")
								imgFile.write(decodedImage)
								imgFile.close()
							a = a + 1

						a = 0

						while a != len(df.index):
							encodedDisegno = df.loc[a, "disegno"]
							if encodedDisegno == encodedDisegno:
								decodedDisegno = base64.b64decode(encodedDisegno)
								if not os.path.exists(unzippedFolder + "/Disegno persiane"):
									os.makedirs(unzippedFolder + "/Disegno persiane")
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] + {} +
									# ".png".format(a)
									disegnoName = f"{unzippedFolder}/Disegno persiane/{df['riferimento'].values[a]}{a}.png"
								else:
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] + {} +
									# ".png".format(a)
									disegnoName = f"{unzippedFolder}/Disegno persiane/{df['riferimento'].values[a]}{a}.png"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "disegno"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Disegno persiane/{df['riferimento'].values[a]}{a}.png\"; \"{df['riferimento'].values[a]}{a}.png\")"
								imgFile = open(disegnoName, "wb")
								imgFile.write(decodedDisegno)
								imgFile.close()
							a = a + 1

						a = 0

						while a != len(df.index):
							encodedVideo = df.loc[a, "audioVideo"]
							if encodedVideo == encodedVideo:
								decodedVideo = base64.b64decode(encodedVideo)
								if not os.path.exists(unzippedFolder + "/Audio persiane"):
									os.makedirs(unzippedFolder + "/Audio persiane")
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] +
									# {} + ".png".format(a)
									videoName = f"{unzippedFolder}/Audio persiane/{df['riferimento'].values[a]}{a}.mp4"
								else:
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] +
									# {} + ".png".format(a)
									videoName = f"{unzippedFolder}/Audio persiane/{df['riferimento'].values[a]}{a}.mp4"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "audioVideo"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Audio persiane/{df['riferimento'].values[a]}{a}.mp4\"; \"{df['riferimento'].values[a]}{a}.mp4\")"
								imgFile = open(videoName, "wb")
								imgFile.write(decodedVideo)
								imgFile.close()
							a = a + 1

						a = 0

						# updating the column value/data
						# df["blob"] = ""
						# df["disegno"] = ""

						# writing into the file
						# df.to_csv(zip_dir + "/" + zip_name + "/Configurazione Persiane.csv", index=False, sep=";")

						os.remove(unzippedFolder + "/configurazionePersiane.csv")

						df_merged1 = df1.merge(df, how="inner", left_on=["id"], right_on="idParente")

						df_merged1["id_y"] = ""
						df_merged1["idParente"] = ""

						# cancella le colonne
						df_merged1.drop(["id_y", "idParente"], axis="columns", inplace=True)
						df_merged1.drop(["larghezzaCassonetto"], axis="columns", inplace=True)
						df_merged1.drop(["altezzaCassonetto"], axis="columns", inplace=True)
						df_merged1.drop(["spessoreCassonetto"], axis="columns", inplace=True)
						df_merged1.drop(["profonditaCielino"], axis="columns", inplace=True)

						df_merged1.rename({"id_x": "id", "blob": "immagini"}, axis="columns", inplace=True)

						os.remove(unzippedFolder + "/persiane.csv")

						# persiane + configurazionePersiane
						csv_persiane = df_merged1.to_csv(zip_dir + "/" + zip_name + "/Persiane.csv", index=False,
														 sep=";")
						print(df)

				# TODO: ALLARGARE AUTOMATICAMENTE LE COLONNE
				#   df_merged1.to_excel(zip_dir + "/" + zip_name + "/Persiane.xlsx", index=False, header=True)
				#   writer = pd.ExcelWriter(zip_dir + "/" + zip_name + "/Persiane.xlsx", engine="openpyxl")
				#   df_excel = pd.read_excel(zip_dir + "/" + zip_name + "/Persiane.xlsx", engine="openpyxl")
				#   for column in df_excel:
				#     column_length = max(df[column].astype(str).map(len).max(), len(column))
				#     col_idx = df.columns.get_loc(column)
				#     writer.sheets['Persiane'].set_column(col_idx, col_idx, column_length)
				#   writer.save()

				if esiste_tapparelle:
					if os.path.exists(unzippedFolder + "/configurazioneTapparelle.csv"):
						df = pd.read_csv(unzippedFolder + "/configurazioneTapparelle.csv", sep=";")

						while a != len(df.index):
							encodedImage = df.loc[a, "blob"]
							if encodedImage == encodedImage:
								decodedImage = base64.b64decode(encodedImage)
								if not os.path.exists(unzippedFolder + "/Foto tapparelle"):
									os.makedirs(unzippedFolder + "/Foto tapparelle")
									# imageName = (unzippedFolder + "/Foto tapparelle/" + df["riferimento"].values[a] + {} +
									# ".jpg").format(a)
									imageName = f"{unzippedFolder}/Foto tapparelle/{df['riferimento'].values[a]}{a}.jpg"
								else:
									# imageName = (unzippedFolder + "/Foto tapparelle/" + df["riferimento"].values[a] + {} +
									# ".jpg").format(a)
									imageName = f"{unzippedFolder}/Foto tapparelle/{df['riferimento'].values[a]}{a}.jpg"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "blob"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Foto tapparelle/{df['riferimento'].values[a]}{a}.jpg\"; \"{df['riferimento'].values[a]}{a}.jpg\")"
								imgFile = open(imageName, "wb")
								imgFile.write(decodedImage)
								imgFile.close()
							a = a + 1

						a = 0

						while a != len(df.index):
							encodedDisegno = df.loc[a, "disegno"]
							if encodedDisegno == encodedDisegno:
								decodedDisegno = base64.b64decode(encodedDisegno)
								if not os.path.exists(unzippedFolder + "/Disegno tapparelle"):
									os.makedirs(unzippedFolder + "/Disegno tapparelle")
									# disegnoName = unzippedFolder + "/Disegno tapparelle/" + df["riferimento"].values[a]
									# + {} + ".png".format(a)
									disegnoName = f"{unzippedFolder}/Disegno tapparelle/{df['riferimento'].values[a]}{a}.png"
								else:
									# disegnoName = unzippedFolder + "/Disegno tapparelle/" + df["riferimento"].values[a]
									# + {} + ".png".format(a)
									disegnoName = f"{unzippedFolder}/Disegno tapparelle/{df['riferimento'].values[a]}{a}.png"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "disegno"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Disegno tapparelle/{df['riferimento'].values[a]}{a}.png\"; \"{df['riferimento'].values[a]}{a}.png\")"
								imgFile = open(disegnoName, "wb")
								imgFile.write(decodedDisegno)
								imgFile.close()
							a = a + 1

						a = 0

						while a != len(df.index):
							encodedVideo = df.loc[a, "audioVideo"]
							if encodedVideo == encodedVideo:
								decodedVideo = base64.b64decode(encodedVideo)
								if not os.path.exists(unzippedFolder + "/Audio tapparelle"):
									os.makedirs(unzippedFolder + "/Audio tapparelle")
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] +
									# {} + ".png".format(a)
									videoName = f"{unzippedFolder}/Audio tapparelle/{df['riferimento'].values[a]}{a}.mp4"
								else:
									# disegnoName = unzippedFolder + "/Disegno persiane/" + df["riferimento"].values[a] +
									# {} + ".png".format(a)
									videoName = f"{unzippedFolder}/Audio tapparelle/{df['riferimento'].values[a]}{a}.mp4"
								# cambia il valore nelle celle della colonna blob con indice a

								df.loc[
									a, "audioVideo"] = f"=COLLEG.IPERTESTUALE(\"{unzippedFolder}/Audio tapparelle/{df['riferimento'].values[a]}{a}.mp4\"; \"{df['riferimento'].values[a]}{a}.mp4\")"
								imgFile = open(videoName, "wb")
								imgFile.write(decodedVideo)
								imgFile.close()
							a = a + 1

						a = 0
						# updating the column value/data
						# df["blob"] = ""
						# df["disegno"] = ""

						# writing into the file
						# df.to_csv(zip_dir + "/" + zip_name + "/Configurazione Tapparelle.csv", index=False, sep=";")

						df_merged2 = df2.merge(df, how="inner", left_on=["id"], right_on="idParente")

						df_merged2["id_y"] = ""
						df_merged2["idParente"] = ""

						# cancella le colonne
						df_merged2.drop(["id_y", "idParente"], axis="columns", inplace=True)

						df_merged2.rename({"id_x": "id", "blob": "immagini"}, axis="columns", inplace=True)

						os.remove(unzippedFolder + "/tapparelle.csv")
						os.remove(unzippedFolder + "/configurazioneTapparelle.csv")

						# tapparelle + configurazioneTapparelle
						csv_tapparelle = df_merged2.to_csv(zip_dir + "/" + zip_name + "/Tapparelle.csv", index=False,
														   sep=";")

				Sg.popup_ok("Terminato", keep_on_top=True)

				os.startfile(unzippedFolder)
				# os.startfile(csv_tapparelle)
				# os.startfile(csv_persiane)

				# if returned_value == "OK":
				#     os.startfile(unzippedFolder)

				print(values["-IN-"])

			elif event == "Seleziona cartella":
				print(values["-IN-"])
		except Exception as e:
			# Sg.popup_error_with_traceback(f'Errore.', e)
			print(e)

	window.close()
	return render(request, 'blog/post_list.html', {})