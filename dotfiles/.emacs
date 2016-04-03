


;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)
(add-to-list 'package-archives '("marmalade" . "https://marmalade-repo.org/packages/"))
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))
(add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/") t)


;; edit text template files in html mode
(add-to-list 'auto-mode-alist '("\\.tt$" . html-mode))

;; disabling keybinds of ergoemacs and cua mode
;;(ergoemacs-mode 0)
;;(cua-mode 0)

;; do not make backup files
(setq make-backup-files nil)

(load-theme 'desert t t)
(enable-theme 'desert)

;; Make our default background gray
;;(add-to-list 'default-frame-alist '(background-color . "lightgray"))

;; displays the time in the status bar
(display-time)


(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(column-number-mode t)
 '(custom-enabled-themes (quote (wombat)))
 '(custom-safe-themes
   (quote
    ("f3b838031ef46ae7fd0ec69aa78f411ee5e2e7135d2c661d7ab3b226f1271726" default)))
 '(inhibit-startup-screen t)
 '(package-selected-packages (quote (powershell yaml-mode ergoemacs-mode))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
