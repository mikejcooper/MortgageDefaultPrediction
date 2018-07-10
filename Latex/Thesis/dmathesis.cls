% This is the dmathesis class that gives a format of the thesis
% according to the university of Durham regulation.  To use it, say
% \documentclass{dmathesis} 

% You need to supply file format.tex, where you define the packages
% you want to use etc.

% Good luck and save your time!

% Written by M. Imran and last modified on 2001/06/18.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{dmathesis}[2001/06/18 Durham Maths thesis class]

%  Here the fontsize you can use.

\newcommand\@dmathesisptsize{12pt}

\DeclareOption{12pt}{\renewcommand\@dmathesisptsize{12pt}}
\DeclareOption{11pt}{\renewcommand\@dmathesisptsize{11pt}}
\DeclareOption{10pt}{\renewcommand\@dmathesisptsize{10pt}}


\ProcessOptions

\LoadClass[\@dmathesisptsize,a4paper]{report}

\pagestyle{plain}

%  Here the page setup based on the university of Durham regulation 
\setlength{\voffset}{-1in}  
\setlength{\marginparsep}{0in}  
\setlength{\marginparwidth}{0in}  
\setlength{\marginparpush}{0in}  
\setlength{\hoffset}{-1in}  
\setlength{\oddsidemargin}{3.1cm}  
\setlength{\evensidemargin}{0in} 
\setlength{\textwidth}{15cm}
\setlength{\topmargin}{2cm}
\setlength{\headheight}{15pt}
\setlength{\headsep}{16pt}
\setlength{\textheight}{23.8cm}
\setlength{\footskip}{18pt}

%  Redefinition  \tableofcontents  in  report.cls
\makeatletter
\renewcommand\tableofcontents{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\contentsname
        \@mkboth{\contentsname}{\contentsname}}%
    \@starttoc{toc}%
    \if@restonecol\twocolumn\fi
    }

%  Redefinition \listoffigures in report.cls
\renewcommand\listoffigures{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listfigurename
      \@mkboth{\listfigurename}{\listfigurename}}%
    \@starttoc{lof}%
    \if@restonecol\twocolumn\fi
    }

% %  Redefinition \listoftables in report.cls
\renewcommand\listoftables{%
    \if@twocolumn
      \@restonecoltrue\onecolumn
    \else
      \@restonecolfalse
    \fi
    \chapter*{\listtablename
      \@mkboth{\listtablename}{\listtablename}}%
    \@starttoc{lot}%
    \if@restonecol\twocolumn\fi
    }

%  Redefinition thebibliograph in report.cls
% \renewenvironment{thebibliography}[1]
%      {\chapter*{\bibname
%         \@mkboth{\bibname}{\bibname}}%
%       \list{\@biblabel{\@arabic\c@enumiv}}%
%           {\settowidth\labelwidth{\@biblabel{#1}}%
%             \leftmargin\labelwidth
%             \advance\leftmargin\labelsep
%             \@openbib@code
%             \usecounter{enumiv}%
%             \let\p@enumiv\@empty
%             \renewcommand\theenumiv{\@arabic\c@enumiv}}%
%       \sloppy
%       \clubpenalty4000
%       \@clubpenalty \clubpenalty
%       \widowpenalty4000%
%       \sfcode`\.\@m}
%      {\def\@noitemerr
%       {\@latex@warning{Empty `thebibliography' environment}}%
%       \endlist}


%  Input the format.tex file.
%\input format.tex
 
%\endinput

% Hyperlinks to contents page 
\usepackage{hyperref}
\hypersetup{
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black
}

% \usepackage{natbib}
\usepackage{longtable}
\usepackage[toc,page]{appendix}
\usepackage[bottom]{footmisc}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{changepage}
\usepackage{enumitem}
\usepackage{float}
\usepackage{lscape} 
\usepackage{booktabs}
\usepackage[demo]{graphicx}
\usepackage{subcaption}
\usepackage{appendix}
\usepackage{blindtext}
\usepackage{chngcntr}
\usepackage{url}

\usepackage{natbib}


\newcommand\citeAY[1]{%
  \citeauthor{#1}~(\citeyear{#1})}

\newcommand\citeY[1]{%
  \citeyear{#1}}

\newcommand\citeA[1]{%
  \citeauthor{#1}}




% Notes
\usepackage[pdftex,dvipsnames]{xcolor}  % Coloured text etc.
\usepackage{xargs}                      % Use more than one optional parameter in a new commands
\usepackage[colorinlistoftodos,prependcaption,textsize=tiny]{todonotes}
\newcommandx{\unsure}[2][1=]{\todo[linecolor=red,backgroundcolor=red!25,bordercolor=red,#1]{#2}}
\newcommandx{\change}[2][1=]{\todo[linecolor=blue,backgroundcolor=blue!25,bordercolor=blue,#1]{#2}}
\newcommandx{\info}[2][1=]{\todo[linecolor=OliveGreen,backgroundcolor=OliveGreen!25,bordercolor=OliveGreen,#1]{#2}}
\newcommandx{\improvement}[2][1=]{\todo[linecolor=Plum,backgroundcolor=Plum!25,bordercolor=Plum,#1]{#2}}
\newcommandx{\thiswillnotshow}[2][1=]{\todo[disable,#1]{#2}}

\newcounter{todocounter} \newcommandx{\todocount}[2][1=]{\stepcounter{todocounter}\todo[linecolor=YellowGreen,backgroundcolor=YellowGreen!25,bordercolor=YellowGreen,#1]{\thetodocounter: #2}}


