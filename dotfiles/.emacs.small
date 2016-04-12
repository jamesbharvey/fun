


;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)
(add-to-list 'package-archives '("marmalade" . "https://marmalade-repo.org/packages/"))
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))
(add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/") t)


;; edit template toolkit files in html mode
(add-to-list 'auto-mode-alist '("\\.tt$" . html-mode))


;; skip the startup message/screen
(setq inhibit-startup-message t)

;; never use hardware tabs
(setq-default indent-tabs-mode nil)

;; disabling keybinds of ergoemacs and cua mode
;;(ergoemacs-mode 0)
;;(cua-mode 0)

;; do not make backup files
(setq make-backup-files nil)

;; displays the time in the status bar
(display-time)

;; start speedbar if we're using a window system
(when window-system (speedbar t))
