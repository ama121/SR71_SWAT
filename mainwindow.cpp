#include <cstdlib>
#include <string>
#include "mainwindow.h"
#include "ui_mainwindow.h"

QT_CHARTS_USE_NAMESPACE

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_analyseButton_clicked()
{
    QProcess process;
    QString tweetFromUser =  ui->tweet->toPlainText();
    QString finalCMD = "python /Users/abhi/SR71_SWAT/UBCcompetition.py "+tweetFromUser;
    process.start("python /Users/abhi/SR71_SWAT/UBCcompetition.py");
    QThread::sleep(3);
    process.waitForFinished(); // will wait forever until finished
    process.close();

    QString stdout = process.readAllStandardOutput();
    QString stderr = process.readAllStandardError();

    QMessageBox::information(this,tr("Tweet"),stdout);

    //ui->tweet->setText(stdout);


    if (stdout.toInt() == 0){
        QPixmap pix("/Users/abhi/SR71_SWAT/obama.jpg");
        ui->picLabel->setPixmap(pix.scaled(150,150));
    }
    else {
        QPixmap pix("/Users/abhi/SR71_SWAT/obamaH.jpg");
        ui->picLabel->setPixmap(pix.scaled(150,150));
    }


}

void MainWindow::on_inputButton_clicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,tr("Open File"),"/User/abhi/Downloads/","CSV File (*.csv)");

    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << file.errorString();
        return;
    }

    int countHappy = 0;
    int countSad = 0;
    float countTot = 0;

    while (!file.atEnd()) {

        QString line = file.readLine();
        //QMessageBox::information(this,tr("Tweet"),line);

        QProcess process;
        QString finalCMD = "python /Users/abhi/SR71_SWAT/UBCcompetition.py "+line;
        process.start("python /Users/abhi/SR71_SWAT/modelScript.py");
        process.waitForFinished(); // will wait forever until finished
        QString stdout = process.readAllStandardOutput();
        QThread::sleep(5);

        if (stdout.toInt() == 1){
            countHappy++;
        }
        else if(stdout.toInt() == 0){
            countSad++;
        }

        countTot++;
    }

    if (countHappy > countSad){
        QPixmap pix("/Users/abhi/SR71_SWAT/obamaH.jpg");
        ui->picLabel->setPixmap(pix.scaled(150,150));
    }
    else{
        QPixmap pix("/Users/abhi/SR71_SWAT/obamaH.jpg");
        ui->picLabel->setPixmap(pix.scaled(150,150));
    }

    QPieSeries *series = new QPieSeries();
    series->append("Happy",countHappy/countTot);
    series->append("Sad",countSad/countTot);

    // Add label to 1st slice
    QPieSlice *slice0 = series->slices().at(0);
    slice0->setLabelVisible();

    // Add label, explode and define brush for 2nd slice
    QPieSlice *slice1 = series->slices().at(1);
    slice1->setExploded();
    slice1->setPen(QPen(Qt::darkGreen, 2));
    slice1->setBrush(Qt::green);

    // Create the chart widget
    QChart *chart = new QChart();

    // Add data to chart with title and hide legend
    chart->addSeries(series);
    chart->setTitle("How Happy is this Person");
    chart->legend()->hide();

    // Used to display the chart
    QChartView *chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);

    ui->chartLayout->addWidget(chartView,0,0);

}
