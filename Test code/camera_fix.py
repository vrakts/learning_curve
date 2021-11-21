ctext1 = ""
ctext2 = ""
# camera_text = "Οπίσθια: 0.3MP (μέσω λογισμικού 1.3MP), flash"
# camera_text = "Οπίσθια: 13MP(f2.2/PDAF) + 2MP(f2.4) + 2MP(f2.4), LED flash, HDR. Εμπρόσθια: 5MP(f2.2)"
# camera_text = "Οπίσθια: 13MP+ 2MP+ 2MP, LED flash, HDR. Εμπρόσθια: 5MP(f2.2)"
# camera_text = "Οπίσθια: 5MP/LED flash/HDR. Εμπρόσθια: 2MP"
# camera_text = "Οπίσθια: 2MP /LED flash. Εμπρόσθια: 2MP /LED flas"
camera_text = "Οπίσθια: 13MP /1.4''/autofocus/LED flash/panorama/HDR. Εμπρόσθια: 8MP /1.4''"
"""
Οπίσθια: 13MP /1.4''/autofocus/LED flash/panorama/HDR. Εμπρόσθια: 8MP /1.4''
"""
print("camera_text: " + camera_text)
while camera_text.find("(") >= 0 :
 ctext1 = camera_text[:camera_text.find("(")].strip()
 ctext2 = camera_text[camera_text.find(")") + 1:].strip()
 print("ctext1 = " + ctext1)
 print("ctext2 = " + ctext2)
 if ctext2.find("(") >= 0 and ctext2.find(")") < 0 :  # υπάρχει το "(" αλλά δεν υπάρχει το ")"
  if ctext2.find(".") > 0 and ctext2.find("MP") > 15 :  # υπάρχει τελεία και τα MP είναι μακριά
   ctext2 = ctext2[ctext2.find("."):]
  else :
   ctext2 = ""
 print("ctext2 = " + ctext2)
 camera_text = ctext1.strip() + ctext2.strip()
 print("camera_text = " + camera_text)
 input()
 print("camera_text.find(',') >= 0 = " + str(camera_text.find(",") >= 0))

while camera_text.find(",") >= 0 :
 ctext1 = camera_text[:camera_text.find(",")].strip()
 ctext2 = camera_text[camera_text.find(","):]
 if ctext2.find(".") >= 0 :
  ctext2 = ctext2[ctext2.find("."):].strip()
 else :
  ctext2 = ""
 print("ctext1: " + ctext1)
 print("ctext2: " + ctext2)
 camera_text = (ctext1 + ctext2).replace("+ ", " + ")
 input()
 print("camera_text: " + camera_text)

while camera_text.find("/") >= 0 :
 ctext1 = camera_text[:camera_text.find("/")].strip()
 ctext2 = camera_text[camera_text.find("/"):].strip()
 if ctext2.find(".") >= 0 :
  ctext2 = ctext2[ctext2.find("."):].strip()
 elif ctext2.find("/") >= 0 :
  ctext2 = ctext2[:ctext2.find("/")].strip()
 else :
  continue
 print("ctext1: " + ctext1)
 print("ctext2: " + ctext2)
 camera_text = (ctext1 + ctext2).replace("+ ", " + ")
 input()
 print("camera_text: " + camera_text)

ctemp = camera_text[camera_text.find("/"):].strip()
if ctemp.find(". Εμπρό") > 0 :
 