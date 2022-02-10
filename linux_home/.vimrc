set nocompatible                " be iMproved
filetype off                    " required!
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

"my Bundle here:
Plugin 'majutsushi/tagbar'
Plugin 'fholgado/minibufexpl.vim'
Plugin 'scrooloose/nerdtree'
Plugin 'airblade/vim-gitgutter'

call vundle#end()            " required
filetype plugin indent on    " required


" ***common setting***
"
" line number
set number
set ruler

" width of a tabstop
" soft just used for backspace
set tabstop=4
set softtabstop=4
" indent
set shiftwidth=4
" tab -> space
set smarttab
set expandtab
set backspace=indent,eol,start  " Backspace

set autoindent
set smartindent
set cindent

" show error for mixed tab-space
let c_space_errors = 1

" <Leader>
let mapleader=";"

" Color synax and font
set background=dark
colorscheme slate

set hlsearch
set incsearch
set cursorline
set cursorcolumn
" 开启语法高亮功能
syntax enable
" " 允许用指定语法高亮配色方案替换默认方案
syntax on
" set line length limit
" set colorcolumn=100

if (has("gui_running"))
	set guifont=Monospace\ 14
	set guifontwide=STHeiti\ 14
	set linespace=6
	set guioptions-=T "隐藏工具栏
endif

" 保存时自动删除行尾多余的空白字符
function! RemoveTrailingSpace()
    if $VIM_HATE_SPACE_ERRORS != '0'
        normal m`
        silent! :%s/\s\+$//e
        normal ``
    endif
endfunction
autocmd BufWritePre * nested call RemoveTrailingSpace()

" ************
" ***Plugin***
" ************

" Tagbar
" 设置 tagbar 子窗口的位置出现在主编辑区的左边
let tagbar_left=1
" 设置显示／隐藏标签列表子窗口的快捷键。速记：identifier list by tag
nnoremap <Leader>lta :TagbarToggle<CR>
" 设置标签子窗口的宽度
let tagbar_width=32
" tagbar 子窗口中不显示冗余帮助信息
let g:tagbar_compact=1

" MiniBufferExplorer
"
" buffer 切换快捷键
map <C-n> :MBEbn<cr>
map <C-p> :MBEbp<cr>
map n<C-p> :MBEbb<cr>
map n<C-n> :MBEbf<cr>

" NERDTree
nmap <Leader>nt :NERDTreeToggle<CR>
" 设置NERDTree子窗口宽度
let NERDTreeWinSize=32
" " 设置NERDTree子窗口位置
let NERDTreeWinPos="right"
" " 显示隐藏文件
let NERDTreeShowHidden=1
" " NERDTree 子窗口中不显示冗余帮助信息
let NERDTreeMinimalUI=1
" " 删除文件时自动删除文件对应 buffer
let NERDTreeAutoDeleteBuffer=1

" git gutter
nmap ]h <Plug>(GitGutterNextHunk)
nmap [h <Plug>(GitGutterPrevHunk)


" cscope
if has('cscope')
  set cscopetag cscopeverbose

  if has('quickfix')
    set cscopequickfix=s-,d-,i-,e-
  endif

  cnoreabbrev csa cs add
  cnoreabbrev csf cs find
  cnoreabbrev csk cs kill
  cnoreabbrev csr cs reset
  cnoreabbrev css cs show
  cnoreabbrev csh cs help

  command -nargs=0 Cscope cs add $VIMSRC/src/cscope.out $VIMSRC/src
  map g<c-\> :cs find 0 <C-R>=expand("<cword>")<CR><CR>
  nmap <C-\>c :cs find c <C-R>=expand("<cword>")<CR><CR>
endif

