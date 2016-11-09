import time
import datetime
clr.AddReference("System.Drawing")
import System.Drawing

capturedir = "c:\\temp\\"
pausebit = 3
exposetime = 30
defaultcam = 0

sundata = ((0,0),
(5,22),
(5,22),
(5,21),
(5,20),
(5,20),
(6,19),
(6,19),
(6,20),
(6,21),
(5,21),
(5,21),
(5,22))

# Choose the ZWO camera. 
def selectcam():
   pass

SharpCap.SelectedCamera.Controls.OutputFormat.Value = 'PNG files (*.png)'
capturemode = ""

while True:
   dt = datetime.datetime.now()
   nowhour = int(dt.strftime('%H'))
   monthnum = int(dt.strftime('%m'))
   tlr = sundata[int(monthnum)][0]   # Morning twilight starts
   tls = sundata[int(monthnum)][1]   # Evening twilight ends
   print("\nMonth num: " + str(monthnum) + ". Dawn: " + str(tlr) + ". Dusk: " + str(tls))

   if nowhour >= tlr and nowhour <= tls:
      # Daytime
      capturemode = "Daytime, Autoexposure"
      print("Daytime: " + str(nowhour))
      SharpCap.SelectedCamera.Controls.Exposure.Automatic = True
      print("exposure is " + str(SharpCap.SelectedCamera.Controls.Exposure.Value))
      
   else:
      # Nighttime
      capturemode = "Night-time, Fixed Exposure"
      
      print("Night-time " + str(nowhour))
      
      SharpCap.SelectedCamera.Controls.Exposure.Automatic = False
      time.sleep(pausebit)
      SharpCap.SelectedCamera = SharpCap.Cameras[defaultcam]
      time.sleep(pausebit)
      SharpCap.SelectedCamera.Controls.Exposure.Value = exposetime
      # SharpCap.SelectedCamera.Controls.Exposure.ExposureMs = exposetime
      
      print("exposure is " + str(SharpCap.SelectedCamera.Controls.Exposure.Value))
        
   SharpCap.SelectedCamera.CaptureSingleFrameTo(capturedir + "capture.png")
   time.sleep(1)
   bm = System.Drawing.Bitmap(capturedir + "capture.png")
   g = System.Drawing.Graphics.FromImage(bm)
   f = System.Drawing.Font("Arial", 14)
   stamp = "http://DunedinAurora.NZ \nSkyCam No 2\n FOV ~70deg, South \n" + capturemode + " " +  str(SharpCap.SelectedCamera.Controls.Exposure.Value) + " seconds\n" + System.DateTime.Now.ToString() + " NZST"
   g.DrawString(stamp, f, System.Drawing.Brushes.Red, System.Drawing.Point(0,0))
   g.Dispose()
   f.Dispose()
    
   try:
      bm.Save(capturedir + "timestamped.png")
   except:
      print("Unable to save image")
   
   bm.Dispose()
# do more with png file here
   print("IMage captured at " + System.DateTime.Now.ToString())
   time.sleep(180)