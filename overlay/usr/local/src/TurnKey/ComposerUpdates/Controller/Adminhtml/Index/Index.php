<?php
namespace TurnKey\ComposerUpdates\Controller\Adminhtml\Index;
class Index extends \Magento\Backend\App\Action
{
    protected $resultPageFactory;
    public function __construct(
        \Magento\Backend\App\Action\Context $context,
        \Magento\Framework\View\Result\PageFactory $resultPageFactory)
    {
        $this->resultPageFactory = $resultPageFactory;        
        return parent::__construct($context);
    }
    
    public function execute()
    {
        $page = $this->resultPageFactory->create();  
        $page->setActiveMenu('TurnKey_ComposerUpdates::a_menu_item');
        $page->getConfig()->getTitle()->prepend(__('Save Magento Marketplace keys'));

        $pubkey = $this->getRequest()->getParam('pubkey');
        $privkey = $this->getRequest()->getParam('privkey');

        if (! $pubkey || ! $privkey) {
            return $page;
        }

        $messageBlock = $page->getLayout()->createBlock(
            'Magento\Framework\View\Element\Messages',
            'notification'
        );

        $outfile = fopen('/var/www/magento/auth.json', 'w');

        if ($outfile) {
            fwrite($outfile, '{"http-basic": {"repo.magento.com": {"username": "' . $pubkey .  '", "password": "' . $privkey . '"}}}');
            fclose($outfile);

            $messageBlock->addSuccess('Your keys were successfully saved at /var/www/magento/auth.json. They can now be used for Magento development tasks.');
        } else {
            $messageBlock->addError('Encountered an error trying to write to /var/www/magento/auth.json. Perhaps the permissions are not www-data:www-data.');
        }

        $page->getLayout()->setChild(
            'content',
            $messageBlock->getNameInLayout(),
            'notification_alias'
        );

        return $page;
    }

    protected function _isAllowed()
    {
        return $this->_authorization->isAllowed('TurnKey_ComposerUpdates::menu_1');
    }
        
}
