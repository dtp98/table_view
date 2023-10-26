import os

folder = "F:\\mktlogin_2023\\resources\\IconBulk"
folder_to = "F:\\mktlogin_2023\\resources\\IconPrimaryColor"
for root, dirs, files in os.walk(folder):
  if len(files):
    for file in files:
      #print()
      fr = open(folder + '\\' + file, 'r')
      f_content = fr.read()
      f_content = f_content.replace('white', "#80cbc4")
      fr.close()
      fw = open(folder_to + '\\' + file, 'w')
      fw.write(f_content)
      fw.close()
      