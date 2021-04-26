mkdir -p ~/.streamlit/echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor=\"#0cf1ed\"\n\
backgroundColor=\"#23272a\"\n\
secondaryBackgroundColor=\"#2c2f33\"\n\
textColor=\"#fafafa\"\n\
" > ~/.streamlit/config.toml
