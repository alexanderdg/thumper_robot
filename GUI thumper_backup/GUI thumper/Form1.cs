using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Timers;
using System.Windows.Forms;
using Newtonsoft.Json;


namespace GUI_thumper
{
    public partial class Form1 : Form
    {
        public static Socket sender;
        public static String Batteryvoltage;
        private BackgroundWorker backgroundWorker1;
        delegate void StringArgReturningVoidDelegate(string text);
        public void DisplayTimeEvent(object source, ElapsedEventArgs e)
        {
            BatteryvoltageTexbox.Text += " Appended text";

        }
        public string FieldText
        {
            get { return BatteryvoltageTexbox.Text; }
            set { BatteryvoltageTexbox.Text = value; }
        }

        private void SetText(string text)
        {
            // InvokeRequired required compares the thread ID of the  
            // calling thread to the thread ID of the creating thread.  
            // If these threads are different, it returns true.  
            if (this.StateTextbox.InvokeRequired)
            {
                StringArgReturningVoidDelegate d = new StringArgReturningVoidDelegate(SetText);
                this.Invoke(d, new object[] { text });
            }
            else
            {
                this.StateTextbox.Text = text;
            }
        }
        System.Net.Sockets.TcpClient clientSocket = new System.Net.Sockets.TcpClient();
        
        public Form1()
        {

            InitializeComponent();
        }

        public void SocketThread(object data)
        {
            BatteryvoltageTexbox.Text = "test";
            System.Timers.Timer myTimer = new System.Timers.Timer();
            myTimer.Elapsed += new ElapsedEventHandler(DisplayTimeEvent);
            myTimer.Interval = 100; // 1000 ms is one second
            myTimer.Start();
            while (true)
            {
                string value = null;
                //int bytesSent = sender.Send(msg);
                byte[] bytes = new byte[1024];
                // Receive the response from the remote device.  
                int bytesRec = sender.Receive(bytes);
                string s = String.Format("{0}V",
                        Encoding.ASCII.GetString(bytes, 0, bytesRec));
                Console.Write("Echoed testttt!! = {0}",
                    s);
                Console.Write(": global variable=");
                Console.Write(Batteryvoltage);
                Console.WriteLine("");
                Batteryvoltage = s;
                SetText("dit is een test die eindelijk slaagd");
                System.Threading.Thread.Sleep(100);
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
            clientSocket.Connect("thumper.local", 50007);
        }

        public static string GetIPAddress(string hostname)
    {
        IPHostEntry host;
        host = Dns.GetHostEntry(hostname);

        foreach (IPAddress ip in host.AddressList)
        {
            if (ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
            {
                //System.Diagnostics.Debug.WriteLine("LocalIPadress: " + ip);
                return ip.ToString();
            }
        }
        return string.Empty;
    }
        public static void SendData(String text)
        {
            byte[] msg = Encoding.ASCII.GetBytes(text);
            int bytesSent = sender.Send(msg);
            
        }

        public static void StartClient(String IPadres)
        {
            // Data buffer for incoming data.  
            byte[] bytes = new byte[1024];

            // Connect to a remote device.  
            try
            {
                // Establish the remote endpoint for the socket.  
                // This example uses port 11000 on the local computer.  
                IPHostEntry ipHostInfo = Dns.GetHostEntry(IPadres);
                IPAddress ipAddress = ipHostInfo.AddressList[0];
                Console.WriteLine("" + ipAddress);
                IPEndPoint remoteEP = new IPEndPoint(ipAddress, 50007);

                // Create a TCP/IP  socket.  
                sender = new Socket(ipAddress.AddressFamily,
                    SocketType.Stream, ProtocolType.Tcp);

                // Connect the socket to the remote endpoint. Catch any errors.  
                try
                {
                    sender.Connect(remoteEP);

                    Console.WriteLine("Socket connected to {0}",
                        sender.RemoteEndPoint.ToString());

                    // Receive the response from the remote device.  
                    int bytesRec = sender.Receive(bytes);
                    Console.WriteLine("Echoed test = {0}",
                        Encoding.ASCII.GetString(bytes, 0, bytesRec));

                    // Release the socket.  
                    //sender.Shutdown(SocketShutdown.Both);
                    //sender.Close();
                    Form1 form = new Form1();
                    Thread newThread = new Thread(form.SocketThread);
                    newThread.Start();
                }
                catch (ArgumentNullException ane)
                {
                    Console.WriteLine("ArgumentNullException : {0}", ane.ToString());
                }
                catch (SocketException se)
                {
                    Console.WriteLine("SocketException : {0}", se.ToString());
                }
                catch (Exception e)
                {
                    Console.WriteLine("Unexpected exception : {0}", e.ToString());
                }

            }
            catch (Exception e)
            {
                Console.WriteLine(e.ToString());
            }
        }

        private void ConnectButton_Click(object sender, EventArgs e)
        {
            StartClient(IPaddresTextbox.Text);
        }

        private void BatteryvoltageTexbox_TextChanged(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Console.WriteLine("Send some text to the robot");
        }

        private void RedTrackbar_Scroll(object sender, EventArgs e)
        {
            Thumperdata data = new Thumperdata();
            data.LEDred = RedTrackbar.Value;
            data.LEDgreen = GreenTrackbar.Value;
            data.LEDblue = BlueTrackbar.Value;
            data.MotorMode = 0;
            data.MotorSpeed = 0;
            data.MotorYaw = MotoryawTrackbar.Value;
            string json = JsonConvert.SerializeObject(data);
            //String to_send = "" + RedTrackbar.Value + ":" + GreenTrackbar.Value + ":" + BlueTrackbar.Value;
            SendData(json);
            Console.WriteLine(json);
        }

        private void GreenTrackbar_Scroll(object sender, EventArgs e)
        {
            Thumperdata data = new Thumperdata();
            data.LEDred = RedTrackbar.Value;
            data.LEDgreen = GreenTrackbar.Value;
            data.LEDblue = BlueTrackbar.Value;
            data.MotorMode = 0;
            data.MotorSpeed = 0;
            data.MotorYaw = MotoryawTrackbar.Value;
            string json = JsonConvert.SerializeObject(data);
            //String to_send = "" + RedTrackbar.Value + ":" + GreenTrackbar.Value + ":" + BlueTrackbar.Value;
            SendData(json);
            Console.WriteLine(json);
        }

        private void BlueTrackbar_Scroll(object sender, EventArgs e)
        {
            Thumperdata data = new Thumperdata();
            data.LEDred = RedTrackbar.Value;
            data.LEDgreen = GreenTrackbar.Value;
            data.LEDblue = BlueTrackbar.Value;
            data.MotorMode = 0;
            data.MotorSpeed = 0;
            data.MotorYaw = MotoryawTrackbar.Value;
            string json = JsonConvert.SerializeObject(data);
            //String to_send = "" + RedTrackbar.Value + ":" + GreenTrackbar.Value + ":" + BlueTrackbar.Value;
            SendData(json);
            Console.WriteLine(json);
        }

        private void sendMotorData(int motormode)
        {
            Thumperdata data = new Thumperdata();
            data.LEDred = RedTrackbar.Value;
            data.LEDgreen = GreenTrackbar.Value;
            data.LEDblue = BlueTrackbar.Value;
            data.MotorMode = motormode;
            data.MotorSpeed = MotorspeedTrackbar.Value;
            data.MotorYaw = MotoryawTrackbar.Value;
            string json = JsonConvert.SerializeObject(data);
            SendData(json);
            Console.WriteLine(json);
        }

        private void ForwardButton_Click(object sender, EventArgs e)
        {
            sendMotorData(1);
        }

        private void BackwardButton_Click(object sender, EventArgs e)
        {
            sendMotorData(2);
        }

        private void LeftButton_Click(object sender, EventArgs e)
        {
            sendMotorData(3);
        }

        private void RightButton_Click(object sender, EventArgs e)
        {
            sendMotorData(4);
        }

        private void MotoryawTrackbar_Scroll(object sender, EventArgs e)
        {

        }

        private void StopButton_Click(object sender, EventArgs e)
        {
            Thumperdata data = new Thumperdata();
            data.LEDred = RedTrackbar.Value;
            data.LEDgreen = GreenTrackbar.Value;
            data.LEDblue = BlueTrackbar.Value;
            if (EmergystopCheckbox.Checked)
            {
                data.MotorMode = 5;
            }
            else
            {
                data.MotorMode = 0;
            }
            data.MotorSpeed = 0;
            data.MotorYaw = 0;
            string json = JsonConvert.SerializeObject(data);
            SendData(json);
            Console.WriteLine(json);
        }

        private void StateTextbox_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
    public class Thumperdata
    {

        [JsonProperty("LEDred")]
        public int LEDred { get; set; }

        [JsonProperty("LEDgreen")]
        public int? LEDgreen { get; set; }

        [JsonProperty("LEDblue")]
        public int? LEDblue { get; set; }

        [JsonProperty("MotorMode")]
        public int? MotorMode { get; set; }

        [JsonProperty("MotorSpeed")]
        public int? MotorSpeed { get; set; }

        [JsonProperty("MotorYaw")]
        public int? MotorYaw { get; set; }
    }

    public class Data
    {

        [JsonProperty("thumperdata")]
        public IList<Thumperdata> thumperdata { get; set; }
    }
}
