# Apartado LaTeX de la entrega

En este directorio se encuentra todo lo necesario para crear el fichero que se pide en el apartado **c** de la documentación a entregar. Se pide un documento en word pero se me dió permiso para usar LaTeX.

## Generación del documento

Se proporciona un script, `build.sh`, pero básicamente solo se ejecuta el comando siguiente:

```bash
pdflatex -jobname="49274537G-entregable2-pcd" main.tex
```

Para ejecutarlo se necesitará tener LaTeX instalado en una máquina Linux y tener los paquetes usados instalados. Se puede seguir [este enlace](https://rowannicholls.github.io/sublime_text/latex.html) para instalar lo necesario (no hace falta hacer la parte de ST si no se quiere).

## Borrado de basura

El comando `pdflatex` crea muchos documentos en el proceso, por lo que se proporciona un script, `clean.sh` para eliminar los documentos innecesarios. El script básicamente solo ejecuta el comando siguiente:

```bash
rm "49274537G-entregable2-pcd.aux" "49274537G-entregable2-pcd.log" "49274537G-entregable2-pcd.out"
```

## DISCLAIMER

Aunque no se debería hacer, se deja el documento generado en el repositorio por si el profesor tiene algún problema con la generación del mismo.

## TODO

- Patrones de diseño explicados.
- Dos tags.
- Capturas de lo anterior.
