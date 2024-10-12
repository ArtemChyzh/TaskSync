using System.Text;
using System.Windows;
using System.Net.Http;
using System.Windows.Controls;
using System.Windows.Media;

namespace TestClient
{
    public partial class MainWindow : Window
    {
        private static readonly HttpClient client = new HttpClient();

        public MainWindow()
        {
            InitializeComponent();
        }

        private async void SendButton_Click(object sender, RoutedEventArgs e)
        {
            string url = UrlTextBox.Text;
            string method = ((ComboBoxItem)MethodComboBox.SelectedItem).Content.ToString();
            string requestJson = RequestJsonTextBox.Text;

            try
            {
                HttpResponseMessage responseJson = null;
                switch (method)
                {
                    case "GET":
                        responseJson = await client.GetAsync(url);
                        break;
                    case "POST":
                        responseJson = await client.PostAsync(url, new StringContent(requestJson, Encoding.UTF8, "application/json"));
                        break;
                    case "PUT":
                        responseJson = await client.PutAsync(url, new StringContent(requestJson, Encoding.UTF8, "application/json"));
                        break;
                    case "DELETE":
                        responseJson = await client.DeleteAsync(url);
                        break;
                }

                string responseBody = await responseJson.Content.ReadAsStringAsync();
                ResponseJsonTextBox.Text = responseBody;
                StatusTextBlock.Text = $"Status: {responseJson.StatusCode} ({(int)responseJson.StatusCode})";
                StatusTextBlock.Foreground = responseJson.IsSuccessStatusCode ? Brushes.Green : Brushes.Red;
            }
            catch (Exception ex)
            {
                ResponseJsonTextBox.Text = "Error: " + ex.Message;
                StatusTextBlock.Text = "Status: Error";
                StatusTextBlock.Foreground = Brushes.Red;
            }
        }
    }
}