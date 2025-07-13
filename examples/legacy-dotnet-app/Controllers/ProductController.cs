using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web.Mvc;
using LegacyApp.Models;
using LegacyApp.Services;

namespace LegacyApp.Controllers
{
    public class ProductController : Controller
    {
        private readonly IProductService _productService;
        private readonly ILogger _logger;

        public ProductController(IProductService productService, ILogger logger)
        {
            _productService = productService;
            _logger = logger;
        }

        // GET: Product
        public ActionResult Index()
        {
            try
            {
                var products = _productService.GetAllProducts();
                return View(products);
            }
            catch (Exception ex)
            {
                _logger.LogError("Error retrieving products", ex);
                return new HttpStatusCodeResult(HttpStatusCode.InternalServerError);
            }
        }

        // GET: Product/Details/5
        public ActionResult Details(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            var product = _productService.GetProductById(id.Value);
            if (product == null)
            {
                return HttpNotFound();
            }

            return View(product);
        }

        // GET: Product/Create
        public ActionResult Create()
        {
            return View();
        }

        // POST: Product/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([Bind(Include = "Id,Name,Price,Description")] Product product)
        {
            if (ModelState.IsValid)
            {
                _productService.CreateProduct(product);
                return RedirectToAction("Index");
            }

            return View(product);
        }

        // GET: Product/Edit/5
        public ActionResult Edit(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            var product = _productService.GetProductById(id.Value);
            if (product == null)
            {
                return HttpNotFound();
            }

            return View(product);
        }

        // POST: Product/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit([Bind(Include = "Id,Name,Price,Description")] Product product)
        {
            if (ModelState.IsValid)
            {
                _productService.UpdateProduct(product);
                return RedirectToAction("Index");
            }

            return View(product);
        }

        // GET: Product/Delete/5
        public ActionResult Delete(int? id)
        {
            if (id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }

            var product = _productService.GetProductById(id.Value);
            if (product == null)
            {
                return HttpNotFound();
            }

            return View(product);
        }

        // POST: Product/Delete/5
        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public ActionResult DeleteConfirmed(int id)
        {
            _productService.DeleteProduct(id);
            return RedirectToAction("Index");
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                // Dispose resources if needed
            }
            base.Dispose(disposing);
        }
    }
} 