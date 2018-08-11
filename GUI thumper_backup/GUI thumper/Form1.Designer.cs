namespace GUI_thumper
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.ConnectButton = new System.Windows.Forms.Button();
            this.panel1 = new System.Windows.Forms.Panel();
            this.DisconnectButton = new System.Windows.Forms.Button();
            this.StateTextbox = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.IPaddresTextbox = new System.Windows.Forms.TextBox();
            this.BatteryvoltageTexbox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.button1 = new System.Windows.Forms.Button();
            this.RedTrackbar = new System.Windows.Forms.TrackBar();
            this.GreenTrackbar = new System.Windows.Forms.TrackBar();
            this.BlueTrackbar = new System.Windows.Forms.TrackBar();
            this.MotorspeedTrackbar = new System.Windows.Forms.TrackBar();
            this.panel2 = new System.Windows.Forms.Panel();
            this.label4 = new System.Windows.Forms.Label();
            this.ForwardButton = new System.Windows.Forms.Button();
            this.BackwardButton = new System.Windows.Forms.Button();
            this.RightButton = new System.Windows.Forms.Button();
            this.LeftButton = new System.Windows.Forms.Button();
            this.panel3 = new System.Windows.Forms.Panel();
            this.label5 = new System.Windows.Forms.Label();
            this.MotoryawTrackbar = new System.Windows.Forms.TrackBar();
            this.label6 = new System.Windows.Forms.Label();
            this.StopButton = new System.Windows.Forms.Button();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.EmergystopCheckbox = new System.Windows.Forms.CheckBox();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.RedTrackbar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.GreenTrackbar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.BlueTrackbar)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.MotorspeedTrackbar)).BeginInit();
            this.panel2.SuspendLayout();
            this.panel3.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.MotoryawTrackbar)).BeginInit();
            this.SuspendLayout();
            // 
            // ConnectButton
            // 
            this.ConnectButton.Location = new System.Drawing.Point(3, 341);
            this.ConnectButton.Name = "ConnectButton";
            this.ConnectButton.Size = new System.Drawing.Size(172, 38);
            this.ConnectButton.TabIndex = 0;
            this.ConnectButton.Text = "Connect";
            this.ConnectButton.UseVisualStyleBackColor = true;
            this.ConnectButton.Click += new System.EventHandler(this.ConnectButton_Click);
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.SystemColors.ControlDark;
            this.panel1.Controls.Add(this.DisconnectButton);
            this.panel1.Controls.Add(this.ConnectButton);
            this.panel1.Controls.Add(this.StateTextbox);
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Controls.Add(this.IPaddresTextbox);
            this.panel1.Location = new System.Drawing.Point(607, 12);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(181, 426);
            this.panel1.TabIndex = 1;
            // 
            // DisconnectButton
            // 
            this.DisconnectButton.Location = new System.Drawing.Point(3, 385);
            this.DisconnectButton.Name = "DisconnectButton";
            this.DisconnectButton.Size = new System.Drawing.Size(172, 38);
            this.DisconnectButton.TabIndex = 5;
            this.DisconnectButton.Text = "Disconnect";
            this.DisconnectButton.UseVisualStyleBackColor = true;
            // 
            // StateTextbox
            // 
            this.StateTextbox.Location = new System.Drawing.Point(3, 72);
            this.StateTextbox.Name = "StateTextbox";
            this.StateTextbox.Size = new System.Drawing.Size(175, 20);
            this.StateTextbox.TabIndex = 4;
            this.StateTextbox.TextChanged += new System.EventHandler(this.StateTextbox_TextChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(3, 56);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(32, 13);
            this.label2.TabIndex = 3;
            this.label2.Text = "State";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(3, 12);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(88, 13);
            this.label1.TabIndex = 2;
            this.label1.Text = "IPadres Thumper";
            // 
            // IPaddresTextbox
            // 
            this.IPaddresTextbox.Location = new System.Drawing.Point(3, 28);
            this.IPaddresTextbox.Name = "IPaddresTextbox";
            this.IPaddresTextbox.Size = new System.Drawing.Size(175, 20);
            this.IPaddresTextbox.TabIndex = 2;
            this.IPaddresTextbox.Text = "192.168.0.170";
            // 
            // BatteryvoltageTexbox
            // 
            this.BatteryvoltageTexbox.Location = new System.Drawing.Point(455, 44);
            this.BatteryvoltageTexbox.Name = "BatteryvoltageTexbox";
            this.BatteryvoltageTexbox.Size = new System.Drawing.Size(100, 20);
            this.BatteryvoltageTexbox.TabIndex = 2;
            this.BatteryvoltageTexbox.TextChanged += new System.EventHandler(this.BatteryvoltageTexbox_TextChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(455, 23);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(78, 13);
            this.label3.TabIndex = 3;
            this.label3.Text = "Battery voltage";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(526, 159);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(75, 23);
            this.button1.TabIndex = 4;
            this.button1.Text = "button1";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // RedTrackbar
            // 
            this.RedTrackbar.Location = new System.Drawing.Point(3, 22);
            this.RedTrackbar.Maximum = 100;
            this.RedTrackbar.Name = "RedTrackbar";
            this.RedTrackbar.Size = new System.Drawing.Size(155, 45);
            this.RedTrackbar.TabIndex = 5;
            this.RedTrackbar.Scroll += new System.EventHandler(this.RedTrackbar_Scroll);
            // 
            // GreenTrackbar
            // 
            this.GreenTrackbar.Location = new System.Drawing.Point(3, 61);
            this.GreenTrackbar.Maximum = 100;
            this.GreenTrackbar.Name = "GreenTrackbar";
            this.GreenTrackbar.Size = new System.Drawing.Size(155, 45);
            this.GreenTrackbar.TabIndex = 6;
            this.GreenTrackbar.Scroll += new System.EventHandler(this.GreenTrackbar_Scroll);
            // 
            // BlueTrackbar
            // 
            this.BlueTrackbar.Location = new System.Drawing.Point(3, 110);
            this.BlueTrackbar.Maximum = 100;
            this.BlueTrackbar.Name = "BlueTrackbar";
            this.BlueTrackbar.Size = new System.Drawing.Size(155, 45);
            this.BlueTrackbar.TabIndex = 7;
            this.BlueTrackbar.Scroll += new System.EventHandler(this.BlueTrackbar_Scroll);
            // 
            // MotorspeedTrackbar
            // 
            this.MotorspeedTrackbar.Location = new System.Drawing.Point(10, 150);
            this.MotorspeedTrackbar.Maximum = 255;
            this.MotorspeedTrackbar.Minimum = 50;
            this.MotorspeedTrackbar.Name = "MotorspeedTrackbar";
            this.MotorspeedTrackbar.Size = new System.Drawing.Size(276, 45);
            this.MotorspeedTrackbar.TabIndex = 8;
            this.MotorspeedTrackbar.Value = 50;
            // 
            // panel2
            // 
            this.panel2.BackColor = System.Drawing.SystemColors.ControlLight;
            this.panel2.Controls.Add(this.label4);
            this.panel2.Controls.Add(this.RedTrackbar);
            this.panel2.Controls.Add(this.GreenTrackbar);
            this.panel2.Controls.Add(this.BlueTrackbar);
            this.panel2.Location = new System.Drawing.Point(12, 283);
            this.panel2.Name = "panel2";
            this.panel2.Size = new System.Drawing.Size(161, 155);
            this.panel2.TabIndex = 9;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(101, 6);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(47, 13);
            this.label4.TabIndex = 8;
            this.label4.Text = "RGB led";
            // 
            // ForwardButton
            // 
            this.ForwardButton.Location = new System.Drawing.Point(104, 8);
            this.ForwardButton.Name = "ForwardButton";
            this.ForwardButton.Size = new System.Drawing.Size(88, 40);
            this.ForwardButton.TabIndex = 10;
            this.ForwardButton.Text = "Forward";
            this.ForwardButton.UseVisualStyleBackColor = true;
            this.ForwardButton.Click += new System.EventHandler(this.ForwardButton_Click);
            // 
            // BackwardButton
            // 
            this.BackwardButton.Location = new System.Drawing.Point(104, 85);
            this.BackwardButton.Name = "BackwardButton";
            this.BackwardButton.Size = new System.Drawing.Size(88, 40);
            this.BackwardButton.TabIndex = 11;
            this.BackwardButton.Text = "Backward";
            this.BackwardButton.UseVisualStyleBackColor = true;
            this.BackwardButton.Click += new System.EventHandler(this.BackwardButton_Click);
            // 
            // RightButton
            // 
            this.RightButton.Location = new System.Drawing.Point(198, 47);
            this.RightButton.Name = "RightButton";
            this.RightButton.Size = new System.Drawing.Size(88, 40);
            this.RightButton.TabIndex = 12;
            this.RightButton.Text = "Right";
            this.RightButton.UseVisualStyleBackColor = true;
            this.RightButton.Click += new System.EventHandler(this.RightButton_Click);
            // 
            // LeftButton
            // 
            this.LeftButton.Location = new System.Drawing.Point(10, 47);
            this.LeftButton.Name = "LeftButton";
            this.LeftButton.Size = new System.Drawing.Size(88, 40);
            this.LeftButton.TabIndex = 13;
            this.LeftButton.Text = "Left";
            this.LeftButton.UseVisualStyleBackColor = true;
            this.LeftButton.Click += new System.EventHandler(this.LeftButton_Click);
            // 
            // panel3
            // 
            this.panel3.BackColor = System.Drawing.SystemColors.ControlLight;
            this.panel3.Controls.Add(this.EmergystopCheckbox);
            this.panel3.Controls.Add(this.StopButton);
            this.panel3.Controls.Add(this.label6);
            this.panel3.Controls.Add(this.MotoryawTrackbar);
            this.panel3.Controls.Add(this.label5);
            this.panel3.Controls.Add(this.ForwardButton);
            this.panel3.Controls.Add(this.LeftButton);
            this.panel3.Controls.Add(this.MotorspeedTrackbar);
            this.panel3.Controls.Add(this.RightButton);
            this.panel3.Controls.Add(this.BackwardButton);
            this.panel3.Location = new System.Drawing.Point(12, 12);
            this.panel3.Name = "panel3";
            this.panel3.Size = new System.Drawing.Size(353, 198);
            this.panel3.TabIndex = 14;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(7, 129);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(38, 13);
            this.label5.TabIndex = 15;
            this.label5.Text = "Speed";
            // 
            // MotoryawTrackbar
            // 
            this.MotoryawTrackbar.Location = new System.Drawing.Point(305, 24);
            this.MotoryawTrackbar.Maximum = 15;
            this.MotoryawTrackbar.Minimum = -15;
            this.MotoryawTrackbar.Name = "MotoryawTrackbar";
            this.MotoryawTrackbar.Orientation = System.Windows.Forms.Orientation.Vertical;
            this.MotoryawTrackbar.Size = new System.Drawing.Size(45, 166);
            this.MotoryawTrackbar.TabIndex = 15;
            this.MotoryawTrackbar.Scroll += new System.EventHandler(this.MotoryawTrackbar_Scroll);
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(295, 8);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(55, 13);
            this.label6.TabIndex = 15;
            this.label6.Text = "MotorYaw";
            // 
            // StopButton
            // 
            this.StopButton.Location = new System.Drawing.Point(104, 47);
            this.StopButton.Name = "StopButton";
            this.StopButton.Size = new System.Drawing.Size(88, 40);
            this.StopButton.TabIndex = 16;
            this.StopButton.Text = "Stop";
            this.StopButton.UseVisualStyleBackColor = true;
            this.StopButton.Click += new System.EventHandler(this.StopButton_Click);
            // 
            // richTextBox1
            // 
            this.richTextBox1.Location = new System.Drawing.Point(335, 318);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.Size = new System.Drawing.Size(126, 32);
            this.richTextBox1.TabIndex = 15;
            this.richTextBox1.Text = "";
            this.richTextBox1.TextChanged += new System.EventHandler(this.richTextBox1_TextChanged);
            // 
            // EmergystopCheckbox
            // 
            this.EmergystopCheckbox.AutoSize = true;
            this.EmergystopCheckbox.Location = new System.Drawing.Point(10, 12);
            this.EmergystopCheckbox.Name = "EmergystopCheckbox";
            this.EmergystopCheckbox.Size = new System.Drawing.Size(83, 17);
            this.EmergystopCheckbox.TabIndex = 17;
            this.EmergystopCheckbox.Text = "EmergyStop";
            this.EmergystopCheckbox.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.panel3);
            this.Controls.Add(this.panel2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.BatteryvoltageTexbox);
            this.Controls.Add(this.panel1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.RedTrackbar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.GreenTrackbar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.BlueTrackbar)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.MotorspeedTrackbar)).EndInit();
            this.panel2.ResumeLayout(false);
            this.panel2.PerformLayout();
            this.panel3.ResumeLayout(false);
            this.panel3.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.MotoryawTrackbar)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button ConnectButton;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Button DisconnectButton;
        private System.Windows.Forms.TextBox StateTextbox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox IPaddresTextbox;
        private System.Windows.Forms.TextBox BatteryvoltageTexbox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.TrackBar RedTrackbar;
        private System.Windows.Forms.TrackBar GreenTrackbar;
        private System.Windows.Forms.TrackBar BlueTrackbar;
        private System.Windows.Forms.TrackBar MotorspeedTrackbar;
        private System.Windows.Forms.Panel panel2;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button ForwardButton;
        private System.Windows.Forms.Button BackwardButton;
        private System.Windows.Forms.Button RightButton;
        private System.Windows.Forms.Button LeftButton;
        private System.Windows.Forms.Panel panel3;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TrackBar MotoryawTrackbar;
        private System.Windows.Forms.Button StopButton;
        private System.Windows.Forms.RichTextBox richTextBox1;
        private System.Windows.Forms.CheckBox EmergystopCheckbox;
    }
}

