" Install Plugins
call plug#begin('~/.vim/plugged')
Plug 'kien/ctrlp.vim'
Plug 'itchyny/lightline.vim'
Plug 'scrooloose/nerdtree'
Plug 'tpope/vim-fugitive'
Plug 'valloric/matchtagalways'
Plug 'rking/ag.vim'
Plug 'rbgrouleff/bclose.vim'
call plug#end()

" Match Tag Files
let g:mta_filetypes = {
    \ 'html' : 1,
    \ 'xhtml' : 1,
    \ 'xml' : 1,
    \ 'jinja' : 1,
    \}
nnoremap <leader>y :MtaJumpToOtherTag<cr>

" Remap <leader> to space
:let mapleader="\<Space>"

" enable syntax highlighting
syntax on
set background=light
colorscheme solarized

" Basic editing and formatting
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab
set backspace=indent,eol,start
set showmatch

" Improve Search
:set ignorecase
:set smartcase
:set infercase
:set hlsearch

" Turn on the mouse if we have one
if has('mouse')
   set mouse=a
endif

" Tags Configuration
:set tags=./tags,tags;
nnoremap <silent><Leader><C-]> <C-w><C-]><C-w>T

" Make page navigation work with iterm `ctrl+[` passthrough
:noremap <C-[>b <C-b>
:noremap <C-[>f <C-f>
:noremap <C-[>d <C-d>

" Buffer Management
set hidden
nnoremap <silent><leader>w :Bclose<cr>
nnoremap <leader>l :ls<CR>:b<space>
:noremap <C-n> :bnext<CR>
:noremap <C-p> :bprev<CR>
:noremap <C-e> :b#<CR>

" Splits
set splitbelow
set splitright
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l

" Highlight trailing white space
:highlight TrailingWhitespace ctermbg=darkred guibg=darkred
:let w:m2=matchadd('TrailingWhitespace', '\s\+$\| \+\ze\t')

" Trim trailing whitespaces on some files
autocmd BufWritePre <buffer> %s/\s\+$//e
" autocmd FileType php,js,scss,twig.html autocmd BufWritePre <buffer> %s/\s\+$//e

" Don't automatically start new comments
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o

" Line Numbers
set number
let &colorcolumn=join(range(101,999), ",")

" Display Status Bar
set laststatus=2

" Ctrl+p Configuration
let g:ctrlp_custom_ignore = '_build$\|\.git$\|public/_assets$\|'
let g:ctrlp_clear_cache_on_exit = 0
let g:ctrlp_cache_dir = $HOME . '/.cache/ctrlp'
let g:ctrlp_match_window = 'bottom,order:btt,min:1,max:10,results:50'
let g:ctrlp_map = '<leader>p'
" let g:ctrlp_by_filename = 1
if executable('ag')
    let g:ctrlp_user_command = 'ag %s -l --nocolor -g ""'
endif

