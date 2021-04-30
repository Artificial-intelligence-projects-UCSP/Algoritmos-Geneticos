#include <iostream>
#include <vector>
#include <string>
#include <bitset>
#include <stdlib.h>
#include <time.h>
#include <stdio.h>


#define lenx 8
#define leny 7
#define ul unsigned long

using namespace std;


string to_bin(ul x, ul y) {
    string res = "";
    res = bitset<lenx>(x).to_string();
    res = res + bitset<leny>(y).to_string();
    //x -> 7
    //y -> 8
    return res;
}   
void to_int(string num, ul& x, ul& y) {
    string sx = num.substr(0, lenx);
    string sy = num.substr(lenx, leny);
    x = bitset<lenx>(sx).to_ulong();
    y = bitset<leny>(sy).to_ulong();
//    cout << sx << " " << x << endl;
  //  cout << sy << " " << y << endl;
}

ul func(ul x, ul y) {
    ul res;
    res = x * x + y * y - 2 * y * x;
    return res;
}



void bubbleSort(vector<string> &p, vector<float> &arr)
{
    int i, j;
    for (i = 0; i < arr.size() - 1; i++)
        for (j = 0; j < arr.size() - i - 1; j++) {
            if (arr[j] < arr[j + 1]) {
                ul tem = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tem;
                string tem1 = p[j];
                p[j] = p[j + 1];
                p[j + 1] = tem1;

            }
        }
}

void mezclar(string& a, string& b) {
    string aux = "01";

    string mascara = "000010000";

    for (int i = 0; i < a.length(); ++i) {
        int xd = rand() % mascara.length();
        if (mascara[xd] == '1') {
            char temp = a[i];
            a[i] = b[i];
            b[i] = temp;
        }
    }
}

vector<string> cruzamiento(vector<string>& padres) {
    int cont = 0;
    int pos = 0;
    vector<string> nuevapoblacion;
    for (int i = 0; i < npoblacion/2; ++i) {
        int r1 = rand() % padres.size();
        int r2 = rand() % padres.size();
        string a, b;
        a = padres[r1];
        b = padres[r2];
        mezclar(a, b);
        nuevapoblacion.push_back(a);
        nuevapoblacion.push_back(b);
    }
    return nuevapoblacion;
}
void seleccion(vector<string> &p, vector<float>& a,float media) {
    int cont = 0; 
    vector<string> padres;
    int pos = 0;
    while (cont < npoblacion && pos!=npoblacion) {
        
        const double repetir = static_cast<int>(a[pos]/media * 1.0 + 0.5) / 1.0;

        for (int i = 0; i < repetir; ++i) {
            padres.push_back(p[pos]);
        }

        cont += repetir;
        pos++;
    }
    vector<string> nuevos = cruzamiento(padres);
    p = nuevos;
}

void algoritmo(ul& x, ul& y) {
    vector<string> poblacion;
    srand(time(NULL));
    for (int i = 0; i < npoblacion; ++i) {
        ul xd = rand() % (2 << (lenx-1));
        ul xy = rand() % (2 << (leny-1));
        poblacion.push_back(to_bin(xd, xy));
    }
    for (int i = 0; i < poblacion.size(); ++i) {
        ul xd, yd;
        to_int(poblacion[i], xd, yd);
        //        cout << poblacion[i] << " " << xd << " " << yd << endl;
    }


    for (int ite = 0; ite < niteraciones; ++ite) {
        float media = 0;
        vector<float> aptitud;
        for (int i = 0; i < npoblacion; ++i) {
            ul xd, yd;
            to_int(poblacion[i], xd, yd);
            ul apt = func(xd, yd);
            aptitud.push_back(apt);
            media += apt;
        }
        media /= npoblacion;
        cout << media << endl;
        bubbleSort(poblacion, aptitud);
        //        for (int i = 0; i < npoblacion; ++i) {
          //          cout << poblacion[i] << " " << aptitud[i] << " " << aptitud[i] / media << " " << endl;
            //    }
        seleccion(poblacion, aptitud, media);

    }
    ul xd, yd;
    to_int(poblacion[0], xd, yd);
    ul xd1, yd1;
    to_int(poblacion[npoblacion - 1], xd1, yd1);
    //cout << poblacion[0] << " " << xd << " " << yd << endl;
    //cout << poblacion[npoblacion - 1] << " " << xd1 << " " << yd1 << endl;
    //cout << func(xd, yd) << endl;
    
    return;
}

int main()
{
    ul x1, y1;
    algoritmo(x1, y1);
    return 0;
}

