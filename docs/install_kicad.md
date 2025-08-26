# Install KiCad Using the Terminal (Recommended)

1. **Open your terminal**.  
   You can use the keyboard shortcut `Ctrl + Alt + T`.

2. **Add the KiCad PPA** for the latest stable release by running the following command:  
   You will be prompted to enter your user password.

   ```sh
   sudo add-apt-repository --yes ppa:kicad/kicad-9.0-releases
   ```

   > **Note:** The version number in the PPA (`kicad-9.0-releases`) will change as new major releases of KiCad become available. For the latest stable version, check the [official KiCad downloads page](https://www.kicad.org/download/) for the correct PPA address.

3. **Update your package list** to include software from the new PPA:

   ```sh
   sudo apt update
   ```

4. **Install KiCad** along with all recommended dependencies (including library files):

   ```sh
   sudo apt install --install-recommends kicad
   ```

5. **Launch KiCad** after installation:  
   - From your application menu, search for *KiCad*, or  
   - Run the following command in the terminal:

     ```sh
     kicad
     ```

---
https://www.kicad.org/download/linux/  

sudo add-apt-repository ppa:kicad/kicad-9.0-releases  
sudo apt update  
sudo apt install kicad  
