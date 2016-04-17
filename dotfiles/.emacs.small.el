




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
